import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
from typing import Optional, Any
import seaborn as sns
import pickle
import dill
from scipy.integrate import odeint
from UQpy.distributions import Uniform, Normal, JointIndependent #, Lognormal
from UQpy.distributions.collection.Lognormal import Lognormal
from UQpy.surrogates import *
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import scipy.stats as stats
from multiprocessing import Pool, cpu_count
from scipy.interpolate import interp1d
import scipy as sc
import joblib
import pyglam as glam


# =============================================================================
# BENCHMARK PIPELINE (R/S problem) — used by benchmark
# =============================================================================

def generate_latent_variables_benchmark(n_latent_samples: int, z1_mean: float = 1.0, z1_std: float = 0.028, z2_mean: float = 1.0, z2_std: float = 0.096) -> tuple[np.ndarray, np.ndarray]:
    """Generates the latent multipliers of the R/S benchmark. Both follow a normal distribution, in line with `generate_latent_variables`.

    :param n_latent_samples: Number of latent samples to generate
    :param z1_mean: Mean of the resistance latent multiplier
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_mean: Mean of the load latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier

    :return: Sampled multipliers z1 (resistance) and z2 (load)
    """

    z1_latent = np.random.normal(loc=z1_mean, scale=z1_std, size=n_latent_samples)
    z2_latent = np.random.normal(loc=z2_mean, scale=z2_std, size=n_latent_samples)

    return z1_latent, z2_latent


def emulator_function_time_benchmark(x: np.ndarray, names_x_variables: list, time_step: float = 0.0, n_latent_samples: int = 1000, k_factor_final: float = 0.3, z1_std: float = 0.028, z2_std: float = 0.096, verbose: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    r"""Compute the emulator of the R/S benchmark state limit function.

    The state limit function is

    .. math::

        g = k(t) \cdot \frac{R}{z_1} - S \cdot z_2

    where :math:`R` is the resistance, :math:`S` is the load, and :math:`z_1` and :math:`z_2` are
    normal latent multipliers. Failure is :math:`g < 0`.

    The degradation factor

    .. math::

        k(t) = 1 + (k_{final} - 1) \, \frac{t}{100}

    shrinks the resistance linearly with time, reaching ``k_factor_final`` at :math:`t = 100`.
    Setting ``k_factor_final`` to 1.0 removes the time effect and leaves the plain
    :math:`g = R/z_1 - S z_2`.

    :param x: Design samples, shape (n_samples, 2) as [R, S]
    :param names_x_variables: Names of the two design variables, used as the identifying columns of the output
    :param time_step: Time step of the analysis, feeding the degradation factor k(t)
    :param n_latent_samples: Number of latent samples per design sample
    :param k_factor_final: Value of the degradation factor at t = 100. Use 1.0 for no time effect
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier
    :param verbose: Whether to print per-sample diagnostics

    :return: [0] = one row per latent replica ; [1] = one row per design point, with the lambdas and the processing time
    """

    dfs = []

    # =========================
    # 0. Degradation factor
    # =========================
    k_factor = 1 + (k_factor_final - 1) * time_step / 100

    for i in range(x.shape[0]):
        # Wall time spent on this design point, used later to measure the emulator speed-up
        t_start = time.perf_counter()

        # =========================
        # 1. Design point properties
        # =========================
        base_r = float(x[i][0])
        base_s = float(x[i][1])

        # =========================
        # 2. Generate latent variables (resistance and load uncertainty)
        # =========================
        z1_latent, z2_latent = generate_latent_variables_benchmark(n_latent_samples, z1_std=z1_std, z2_std=z2_std)

        # =========================
        # 3. Emulator of state limit function g = k(t) * R / z1 - S * z2
        # =========================
        r_effective = k_factor * base_r / z1_latent
        s_effective = base_s * z2_latent
        g_vals      = r_effective - s_effective  # failure if g < 0

        # =========================
        # 4. Create DataFrame
        # =========================
        df = pd.DataFrame({
                            names_x_variables[0]: [x[i, 0]] * n_latent_samples,
                            names_x_variables[1]: [x[i, 1]] * n_latent_samples,
                            'z1_latent': z1_latent,
                            'R_effective': r_effective,
                            'z2_latent': z2_latent,
                            'S_effective': s_effective,
                            'k factor': k_factor,
                            'Time (years)': time_step,
                            'g': g_vals
                        })

        # =========================
        # 5. GLAM fitting
        # =========================
        if np.std(g_vals) < 1e-6:
            lambdas = [np.nan, np.nan, np.nan, np.nan]
        else:
            try:
                emulator = glam.GlamFKML()
                sol = emulator.fit_lambdas(df['g'].values, method="least_squares")
                if sol.status in [-1, -2]:
                    lambdas = [np.nan] * 4
                else:
                    lambdas = sol.x
            except Exception as e:
                if verbose:
                    print(f"  GLAM fitting failed: {e}")
                lambdas = [np.nan] * 4

        df['lambda 1'] = lambdas[0]
        df['lambda 2'] = lambdas[1]
        df['lambda 3'] = lambdas[2]
        df['lambda 4'] = lambdas[3]

        # Cost of producing this design point: latent sampling, g evaluation and GLAM fitting
        df['Processing time (s)'] = time.perf_counter() - t_start

        dfs.append(df)

        if verbose:
            print(f"  Sample {i+1}:")
            print(f"    P(g < 0) = {np.mean(g_vals < 0):.4f}")
            print(f"    Mean g = {np.mean(g_vals):.4f}")

    df_full    = pd.concat(dfs, ignore_index=True)
    id_columns = list(names_x_variables[:2])
    df_unique  = (
                    df_full[id_columns + ['lambda 1', 'lambda 2', 'lambda 3', 'lambda 4', 'Processing time (s)']].drop_duplicates(subset=id_columns).reset_index(drop=True)
                 )

    return df_full, df_unique


def generate_dataset_at_time_benchmark(x_train: np.ndarray, x_val: np.ndarray, time_step: float, n_latent_samples: int = 1000, k_factor_final: float = 0.3, z1_std: float = 0.028, z2_std: float = 0.096, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Run the emulator on the training and validation design samples at a single time step, and save both datasets to disk.

    This is the only stage that draws latent samples and fits the GLD — the expensive part that `Processing time (s)` measures. Splitting it from the PCE fit (`train_and_validate_pce_from_dataset_benchmark`) lets the dataset be generated once, in its own notebook, and the PCE refit or re-validated later without repeating any simulation.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<split>_<time_step>_benchmark.pkl` naming convention, where `<split>` is `train` or `val`.

    :param x_train: Design samples used to later train the PCE, shape (n_samples, 2) as [R, S]
    :param x_val: Independent design samples used to later validate the PCE, shape (n_samples_validation, 2)
    :param time_step: Time step of the analysis, feeding the degradation factor k(t)
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param k_factor_final: Value of the degradation factor at t = 100. Use 1.0 for no time effect
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each split

    :return: Dictionary with the full/unique dataframes for the train and validation splits, the total emulator wall time, and the paths written
    """

    out_dir     = Path(output_dir)
    tag         = f'{time_step}_benchmark'
    emulator_kw = dict(names_x_variables=["r", "s"], time_step=time_step, n_latent_samples=n_latent_samples, k_factor_final=k_factor_final, z1_std=z1_std, z2_std=z2_std, verbose=False)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING DATASET FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    paths          = {}
    result         = {'time_step': time_step, 'paths': paths}
    emulator_time_s = 0.0
    for split, x in (('train', x_train), ('val', x_val)):
        df_full, df_unique = emulator_function_time_benchmark(x=x, **emulator_kw)
        result[f'df_full_{split}']   = df_full
        result[f'df_unique_{split}'] = df_unique
        emulator_time_s             += float(df_unique['Processing time (s)'].sum())

        if save:
            out_dir.mkdir(parents=True, exist_ok=True)
            for kind, frame in (('dataset_full', df_full), ('dataset_unique', df_unique)):
                key         = f'{kind}_{split}'
                paths[key]  = out_dir / f'{n_latent_samples}_{kind}_{split}_{tag}.pkl'
                with open(paths[key], 'wb') as f:
                    dill.dump(frame, f)

        if verbose:
            print(f'  {split}: {len(x)} design points, {df_unique["Processing time (s)"].sum():.2f} s total')

    result['emulator_time_s'] = emulator_time_s

    return result


def train_and_validate_pce_from_dataset_benchmark(df_unique_train: pd.DataFrame, df_unique_val: pd.DataFrame, joint: Any, time_step: float, n_latent_samples: int = 1000, n_lambdas: int = 4, max_degree: int = 3, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Stage 2 of the split benchmark pipeline: fit a PCE metamodel to a previously generated lambda dataset and validate it. Makes no emulator calls and draws no latent samples.

    Companion of `generate_dataset_at_time_benchmark`: takes its saved `dataset_unique` outputs (train and validation splits) and performs the PCE fit and scoring that `train_and_validate_pce_at_time_benchmark` used to do inline with the data generation.

    Artefacts are written to `output_dir` with the same `<n_latent_samples>_<kind>_<time_step>_benchmark.pkl` naming convention as `train_and_validate_pce_at_time_benchmark`, so downstream notebooks that only read the PCE metamodel don't need to change.

    :param df_unique_train: `dataset_unique_train` dataframe, as saved by `generate_dataset_at_time_benchmark`
    :param df_unique_val: `dataset_unique_val` dataframe, as saved by `generate_dataset_at_time_benchmark`
    :param joint: UQpy JointIndependent distribution of R and S, used for the polynomial basis. Must match the one used to draw `df_unique_train`/`df_unique_val`
    :param time_step: Time step of the analysis (bookkeeping and filenames only — the time effect is already baked into the lambdas)
    :param n_latent_samples: Number of latent samples used to generate the dataset. Only used for the filename prefix, to match `generate_dataset_at_time_benchmark`
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param max_degree: Maximum total degree of the polynomial basis
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the fitted PCE and the validation statistics
    """

    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'{time_step}_benchmark'
    id_columns  = ['r', 's']

    if verbose:
        print(f'\n{"-"*40}')
        print(f'TRAINING PCE FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    # =========================
    # 1. PCE metamodel
    # =========================
    x_train           = df_unique_train[id_columns].to_numpy()
    y_train           = df_unique_train[lambda_cols].to_numpy()
    polynomial_basis  = TotalDegreeBasis(joint, max_degree)
    least_squares     = LeastSquareRegression()
    pce_metamodel     = PolynomialChaosExpansion(polynomial_basis=polynomial_basis, regression_method=least_squares)
    pce_metamodel.fit(x_train, y_train)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths['pce_metamodel'] = out_dir / f'{n_latent_samples}_pce_metamodel_{tag}.pkl'
        with open(paths['pce_metamodel'], 'wb') as f:
            dill.dump(pce_metamodel, f)
        if verbose:
            print('1. PCE training dataset has been saved!')

    # =========================
    # 2. Validation
    # =========================
    x_val          = df_unique_val[id_columns].to_numpy()
    y_val_true     = df_unique_val[lambda_cols].to_numpy()
    y_val_pred     = pce_metamodel.predict(x_val)

    mse_per_lambda = [mean_squared_error(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]
    r2_per_lambda  = [r2_score(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]

    stats_row = {f'MSE λ{i+1}': mse_per_lambda[i] for i in range(n_lambdas)}
    stats_row.update({f'R² λ{i+1}': r2_per_lambda[i] for i in range(n_lambdas)})
    statistics_ = pd.DataFrame(stats_row, index=[0])

    if save:
        paths['pce_validation_stats'] = out_dir / f'{n_latent_samples}_pce_validation_stats_{tag}.pkl'
        with open(paths['pce_validation_stats'], 'wb') as f:
            dill.dump(statistics_, f)
        if verbose:
            print('2. PCE statistcs has been saved!')

    return {
             'time_step':     time_step,
             'pce_metamodel': pce_metamodel,
             'statistics':    statistics_,
             'paths':         paths,
           }


def generate_nn_dataset_benchmark(pce_metamodels: list, times: np.ndarray, joint: Any, n_points: int = 5000, n_lambdas: int = 4, n_latent_samples: int = 1000, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Build the (R, S, t) -> lambda dataset used to train a single global NN surrogate, by querying the per-time-step PCE metamodels instead of re-running the stochastic emulator.

    Companion of `train_and_validate_pce_from_dataset_benchmark`: reuses its fitted `pce_metamodel` (one per time step, already fit and validated against the emulator) as a cheap oracle — `pce_metamodel.predict(x)` costs microseconds, versus the emulator's per-point GLAM fit over `n_latent_samples` draws. That lets `n_points` be drawn far denser than the emulator dataset each PCE was itself trained on, at no extra Monte Carlo cost. This distills the `len(times)` separate per-time-step PCEs into training data for a single, continuous-in-t model.

    Artefacts are written to `output_dir` as `<n_latent_samples>_dataset_nn_benchmark.pkl`.

    :param pce_metamodels: Fitted `PolynomialChaosExpansion` models, one per entry of `times`, in the same order (as saved by `train_and_validate_pce_from_dataset_benchmark`)
    :param times: Time steps to stack into the dataset [years], paired positionally with `pce_metamodels`
    :param joint: UQpy JointIndependent distribution of R and S, used to draw the query points fed to each PCE
    :param n_points: Number of (R, S) query points drawn per time step
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param n_latent_samples: Number of latent samples used to fit `pce_metamodels`. Only used for the filename prefix, to match `train_and_validate_pce_from_dataset_benchmark`
    :param output_dir: Directory where the .pkl artefact is written
    :param save: Whether to write the .pkl artefact to disk
    :param verbose: Whether to print the progress of each time step

    :return: Dictionary with the stacked dataframe and the path written
    """

    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING NN DATASET FROM {len(times)} PCE MODELS')
        print(f'{"-"*40}')

    # =========================
    # 1. Query each time step's PCE at fresh (r, s) points
    # =========================
    dfs = []
    for t, pce_metamodel in zip(times, pce_metamodels):
        x      = joint.rvs(n_points)
        y_pred = pce_metamodel.predict(x)

        df = pd.DataFrame(x, columns=['r', 's'])
        df.insert(2, 'Time (years)', t)
        df[lambda_cols] = y_pred
        dfs.append(df)

        if verbose:
            print(f'  t = {t:.2f} years: {n_points} points queried from the PCE')

    df_nn = pd.concat(dfs, ignore_index=True)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths['dataset_nn'] = out_dir / f'{n_latent_samples}_dataset_nn_benchmark.pkl'
        with open(paths['dataset_nn'], 'wb') as f:
            dill.dump(df_nn, f)
        if verbose:
            print('The NN dataset has been saved!')

    return {
             'dataset_nn': df_nn,
             'paths':      paths,
           }


def train_and_validate_nn_lambda_benchmark(df_nn: pd.DataFrame, feature_cols: list = ['r', 's', 'Time (years)'], target_cols: list = ['lambda 1', 'lambda 2'], test_frac: float = 0.2, hidden_layer_sizes: tuple = (64, 64), max_iter: int = 500, n_iter_no_change: int = 15, random_state: int = 42, n_latent_samples: int = 1000, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Fit one MLPRegressor per target lambda on (R, S, t) -> lambda, the global NN counterpart of the per-time-step PCE.

    Companion of `generate_nn_dataset_benchmark`: consumes its stacked dataframe, splits it once across the whole time grid (not per time step), and fits an independent `MLPRegressor` per column of `target_cols`. Mirrors the workflow in the exploratory `old/pce_models.ipynb` notebook, wired through the same save/verbose conventions as the rest of the pipeline. Only `target_cols` (by default lambda 1 and lambda 2) are modelled here — the remaining lambdas are meant to be read back from the emulator dataset directly, not predicted by this function.

    Rows with a NaN in any `target_cols` (design points where the GLD fit failed) are dropped before the split.

    Artefacts are written to `output_dir` as `<n_latent_samples>_nn_<target>_model_benchmark.pkl` (one per target), `<n_latent_samples>_nn_scaler_benchmark.pkl`, and `<n_latent_samples>_nn_validation_stats_benchmark.pkl`.

    :param df_nn: Stacked dataset from `generate_nn_dataset_benchmark`, one row per (design point, time step)
    :param feature_cols: Input columns for the NN, in order
    :param target_cols: Lambda columns to fit one model each for
    :param test_frac: Fraction of the (NaN-dropped) rows held out for validation
    :param hidden_layer_sizes: Hidden layer sizes, shared by every target's MLPRegressor
    :param max_iter: Maximum training iterations per MLPRegressor
    :param n_iter_no_change: Early-stopping patience
    :param random_state: Seed for the split and every MLPRegressor's initialisation
    :param n_latent_samples: Number of latent samples used to build `df_nn`. Only used for the filename prefix, to match `generate_nn_dataset_benchmark`
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the fitted models (one per target), the fitted scaler, the validation statistics, and the paths written
    """

    out_dir   = Path(output_dir)
    df_clean  = df_nn.dropna(subset=target_cols).reset_index(drop=True)
    n_dropped = len(df_nn) - len(df_clean)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'TRAINING NN LAMBDA MODELS')
        print(f'{"-"*40}')
        if n_dropped:
            print(f'  Dropped {n_dropped} row(s) with a NaN target')

    # =========================
    # 1. Split and scale
    # =========================
    X = df_clean[feature_cols].to_numpy()
    y = df_clean[target_cols].to_numpy()

    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=test_frac, random_state=random_state)

    scaler   = StandardScaler()
    x_train_s = scaler.fit_transform(x_train)
    x_val_s   = scaler.transform(x_val)

    if verbose:
        print(f'  {len(x_train)} train rows, {len(x_val)} val rows')

    # =========================
    # 2. One MLPRegressor per target
    # =========================
    models    = {}
    stats_row = {}
    for i, target in enumerate(target_cols):
        model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, early_stopping=True, n_iter_no_change=n_iter_no_change, random_state=random_state)
        model.fit(x_train_s, y_train[:, i])
        y_pred = model.predict(x_val_s)

        stats_row[f'MSE {target}'] = mean_squared_error(y_val[:, i], y_pred)
        stats_row[f'R² {target}']  = r2_score(y_val[:, i], y_pred)
        models[target] = model

        if verbose:
            print(f'  {target}: R² = {stats_row[f"R² {target}"]:.6f}, MSE = {stats_row[f"MSE {target}"]:.5f}, '
                  f'iterations = {model.n_iter_}')

    statistics_ = pd.DataFrame(stats_row, index=[0])

    # =========================
    # 3. Save models, scaler and stats
    # =========================
    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        for target, model in models.items():
            key = target.replace(' ', '_')
            paths[key] = out_dir / f'{n_latent_samples}_nn_{key}_model_benchmark.pkl'
            with open(paths[key], 'wb') as f:
                dill.dump(model, f)

        paths['scaler'] = out_dir / f'{n_latent_samples}_nn_scaler_benchmark.pkl'
        with open(paths['scaler'], 'wb') as f:
            dill.dump(scaler, f)

        paths['nn_validation_stats'] = out_dir / f'{n_latent_samples}_nn_validation_stats_benchmark.pkl'
        with open(paths['nn_validation_stats'], 'wb') as f:
            dill.dump(statistics_, f)

        if verbose:
            print('The NN models, scaler and validation stats have been saved!')

    return {
             'models':     models,
             'scaler':     scaler,
             'statistics': statistics_,
             'paths':      paths,
           }


def generate_rul_dataset_benchmark(r: float, s: float, times: np.ndarray, n_latent_samples: int = 1000, lambda3_fixed: float | None = None, lambda4_fixed: float | None = None, n_glam_samples: int = 10000, input_dir: str | Path = '.', output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Predict lambda 1/2 at a fixed (R, S) across a grid of time steps with the trained global NN, fix lambda 3/4, and draw GLD Monte Carlo samples of g at each time step.

    The raw material for a spaghetti / RUL plot: querying the NN instead of the emulator or a per-time-step PCE means any `(R, S, t)` can be evaluated directly, without picking a PCE for a specific `t` first.

    Loads the artefacts written by `train_and_validate_nn_lambda_benchmark` (``<n_latent_samples>_nn_lambda_1_model_benchmark.pkl``, ``..._nn_lambda_2_model_benchmark.pkl``, ``..._nn_scaler_benchmark.pkl``) from `input_dir`. If `lambda3_fixed`/`lambda4_fixed` are not given, they default to the mean of `lambda 3`/`lambda 4` over `generate_nn_dataset_benchmark`'s own training dataset (``<n_latent_samples>_dataset_nn_benchmark.pkl``), also read from `input_dir` — both lambdas vary little with `(R, S, t)`, which is why they aren't modelled by the NN in the first place.

    Artefacts are written to `output_dir` as ``<n_latent_samples>_rul_lambdas_R<r>_S<s>_benchmark.pkl`` (the per-time-step lambda dataframe) and ``<n_latent_samples>_rul_samples_R<r>_S<s>_benchmark.pkl`` (the raw Monte Carlo samples).

    :param r: Fixed resistance value to query
    :param s: Fixed load value to query
    :param times: Time steps to sweep [years]
    :param n_latent_samples: Number of latent samples used to train the NN. Only used for the filename prefix, to match `train_and_validate_nn_lambda_benchmark`
    :param lambda3_fixed: Fixed value for lambda 3. If None, uses the mean over the NN training dataset
    :param lambda4_fixed: Fixed value for lambda 4. If None, uses the mean over the NN training dataset
    :param n_glam_samples: Number of Monte Carlo samples drawn from the GLD at each time step
    :param input_dir: Directory the NN artefacts (and, if needed, the NN training dataset) are read from
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the per-time-step lambda dataframe, the Monte Carlo samples (shape ``(n_glam_samples, len(times))``), the fixed lambda 3/4 used, and the paths written
    """

    in_dir  = Path(input_dir)
    out_dir = Path(output_dir)
    times   = np.asarray(times, dtype=float)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING RUL DATASET AT R={r}, S={s}')
        print(f'{"-"*40}')

    # =========================
    # 1. Load the trained NN (lambda 1, lambda 2) and its scaler
    # =========================
    with open(in_dir / f'{n_latent_samples}_nn_lambda_1_model_benchmark.pkl', 'rb') as f:
        model_l1 = dill.load(f)
    with open(in_dir / f'{n_latent_samples}_nn_lambda_2_model_benchmark.pkl', 'rb') as f:
        model_l2 = dill.load(f)
    with open(in_dir / f'{n_latent_samples}_nn_scaler_benchmark.pkl', 'rb') as f:
        scaler = dill.load(f)

    # =========================
    # 2. Default lambda 3 / lambda 4, if not given
    # =========================
    if lambda3_fixed is None or lambda4_fixed is None:
        with open(in_dir / f'{n_latent_samples}_dataset_nn_benchmark.pkl', 'rb') as f:
            df_nn = dill.load(f)
        if lambda3_fixed is None:
            lambda3_fixed = float(df_nn['lambda 3'].mean())
        if lambda4_fixed is None:
            lambda4_fixed = float(df_nn['lambda 4'].mean())

    if verbose:
        print(f'  lambda 3 fixed at {lambda3_fixed:.4f}, lambda 4 fixed at {lambda4_fixed:.4f}')

    # =========================
    # 3. Predict lambda 1 / lambda 2 across the time grid
    # =========================
    lambda_df    = pd.DataFrame({'r': r, 's': s, 'Time (years)': times})
    query_scaled = scaler.transform(lambda_df[['r', 's', 'Time (years)']].to_numpy())
    lambda_df['lambda 1'] = model_l1.predict(query_scaled)
    lambda_df['lambda 2'] = model_l2.predict(query_scaled)
    lambda_df['lambda 3'] = lambda3_fixed
    lambda_df['lambda 4'] = lambda4_fixed

    # =========================
    # 4. GLD Monte Carlo samples of g at each time step
    # =========================
    samples = np.empty((n_glam_samples, len(times)))
    for i, row in lambda_df.iterrows():
        gld           = glam.GlamFKML(lam1=row['lambda 1'], lam2=row['lambda 2'], lam3=row['lambda 3'], lam4=row['lambda 4'])
        samples[:, i] = gld.rvs(size=n_glam_samples)
        if verbose:
            print(f'  t = {row["Time (years)"]:.1f}: lambda 1 = {row["lambda 1"]:.3f}, lambda 2 = {row["lambda 2"]:.3f}, '
                  f'sample mean = {samples[:, i].mean():.3f}, sample std = {samples[:, i].std():.3f}')

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        tag = f'R{r:g}_S{s:g}_benchmark'
        paths['lambda_df'] = out_dir / f'{n_latent_samples}_rul_lambdas_{tag}.pkl'
        with open(paths['lambda_df'], 'wb') as f:
            dill.dump(lambda_df, f)
        paths['samples'] = out_dir / f'{n_latent_samples}_rul_samples_{tag}.pkl'
        with open(paths['samples'], 'wb') as f:
            dill.dump(samples, f)
        if verbose:
            print('The RUL lambda dataframe and Monte Carlo samples have been saved!')

    return {
             'lambda_df':     lambda_df,
             'samples':       samples,
             'times':         times,
             'r':             r,
             's':             s,
             'lambda3_fixed': lambda3_fixed,
             'lambda4_fixed': lambda4_fixed,
             'paths':         paths,
           }


def compute_rul_benchmark(samples: np.ndarray, times: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    """Time-to-failure for each Monte Carlo sample path, by linear interpolation of the first down-crossing of `threshold`.

    Failure is the state limit function :math:`g` dropping to or below `threshold` (0 by default). A sample path that never crosses is right-censored at the last time step, rather than dropped, so `failure_times.mean()` slightly underestimates the true mean when censoring is frequent — check how many samples hit `times[-1]` exactly before trusting the tail of the distribution.

    :param samples: GLD Monte Carlo realizations, shape ``(n_samples, n_times)``, as returned by `generate_rul_dataset_benchmark`
    :param times: Time steps matching the columns of `samples`
    :param threshold: Failure threshold on the state limit function (failure is :math:`g \\le` `threshold`)

    :return: Failure time per sample, shape ``(n_samples,)``
    """

    times          = np.asarray(times, dtype=float)
    n_samples      = samples.shape[0]
    failure_times  = np.full(n_samples, times[-1], dtype=float)

    for i in range(n_samples):
        path = samples[i]
        for t in range(1, len(times)):
            if path[t] <= threshold < path[t - 1]:
                frac              = (threshold - path[t - 1]) / (path[t] - path[t - 1])
                failure_times[i]  = times[t - 1] + frac * (times[t] - times[t - 1])
                break

    return failure_times


# =============================================================================
# DURABILITY PIPELINE (real problem) — used by durability_final
# =============================================================================

def co2_percentage_1900_1950(year: int) -> float:
    """CO2 atmospheric concentration (%) for historical period 1900–1950. Based on a linear approximation of the upward trend during this period.

    :param year: Calendar year (1900 <= year <= 1950)

    :return: CO2 concentration in percentage (ppm / 10000)
    """

    if not 1900 <= year <= 1950:
        raise ValueError("Year must be between 1900 and 1950 for this function.")

    co2_ppm = 296.0 + 0.30 * (year - 1900)
    return co2_ppm / 1e4


def co2_percentage_1950_2000(year: int) -> float:
    """CO2 atmospheric concentration (%) for historical period 1950–2000. Based on a linear approximation of the accelerating upward trend.

    :param year: Calendar year (1950 <= year <= 2000)

    :return: CO2 concentration in percentage (ppm / 10000)
    """

    if not 1950 <= year <= 2000:
        raise ValueError("Year must be between 1950 and 2000 for this function.")

    co2_ppm = 311.0 + 1.16 * (year - 1950)
    return co2_ppm / 1e4


def co2_percentage_pos2000(year: int) -> float:
    """CO2 atmospheric concentration (%) for post-2000 period. Captures the non-linear (quadratic) acceleration in CO2 buildup observed in recent decades.

    :param year: Calendar year (>= 2000)

    :return: CO2 concentration in percentage (ppm / 10000)
    """

    if year < 2000:
        raise ValueError("Year must be >= 2000 for this function.")

    t  = year - 2000
    C0 = 369.0   # ppm in 2000 (approximate observed value)
    a  = 1.85    # ppm/year (linear component)
    b  = 0.018   # ppm/year² (quadratic component)
    co2_ppm = C0 + a * t + b * t**2

    return co2_ppm / 1e4


def co2_percentage_year(year: int) -> float:
    """Global average atmospheric CO2 concentration (%) valid from 1900 onwards. Routes the calculation to the correct historical formula based on the year.

    :param year: Calendar year (>= 1900)

    :return: CO2 concentration in percentage (ppm / 10000)
    """

    if year < 1900:
        raise ValueError(f"Year must be >= 1900. Received: {year}")

    if year <= 1950:
        return co2_percentage_1900_1950(year)
    elif 1950 < year <= 2000:
        return co2_percentage_1950_2000(year)
    else:
        return co2_percentage_pos2000(year)


def generate_latent_variables(n_latent_samples: int, mean: float = 1.0, cov: float = 0.02) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generates the latent multipliers related to the beam problem. All three follow a normal distribution with the same mean and coefficient of variation.

    :param n_latent_samples: Number of latent samples to generate
    :param mean: Mean of the latent multipliers
    :param cov: Coefficient of variation of the latent multipliers

    :return: Sampled multipliers for relative humidity, concrete compressive strength, and concrete cover
    """

    scale      = cov * mean
    cov_latent = np.random.normal(loc=mean, scale=scale, size=n_latent_samples)
    rh_latent  = np.random.normal(loc=mean, scale=scale, size=n_latent_samples)
    fck_latent = np.random.normal(loc=mean, scale=scale, size=n_latent_samples)

    return rh_latent, fck_latent, cov_latent


def _interp_profile_at(calendar_years: np.ndarray, depths: np.ndarray, year_query: float) -> np.ndarray:
    """Linear interpolation (with linear extrapolation outside the range) of a batch of
    cumulative-max carbonation profiles at a single query year, vectorized across rows.

    :param calendar_years: Grid of calendar years shared by every row, sorted ascending
    :param depths: Carbonation depth profile per row, shape (n_rows, n_grid)
    :param year_query: Calendar year at which to evaluate every row

    :return: Interpolated carbonation depth for each row
    """

    n_grid = len(calendar_years)
    if n_grid == 1:
        return depths[:, 0].copy()

    k = int(np.clip(np.searchsorted(calendar_years, year_query, side='right') - 1, 0, n_grid - 2))
    t0, t1 = calendar_years[k], calendar_years[k + 1]
    frac = 0.0 if t1 == t0 else (year_query - t0) / (t1 - t0)

    return depths[:, k] + frac * (depths[:, k + 1] - depths[:, k])


def emulator_function_time_durability(x: np.ndarray, names_x_variables: list, carb_model: Any, cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2, time_step: float = 0.0, n_latent_samples: int = 1000, verbose: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute the emulator of carbonation depth for durability analysis of reinforced concrete sections.
    """

    dfs = []
    start_year = installation_year
    year_query = start_year + time_step

    # =========================
    # 0. Time grid and CO2(%) profile
    # =========================
    lifetime_full  = 150
    grid_step      = 10
    grid_max       = min(lifetime_full, grid_step * (int(np.ceil(max(time_step, 0) / grid_step)) + 1))
    years          = np.arange(0, grid_max + 1, grid_step)
    calendar_years = start_year + years
    co2_values     = np.array([co2_percentage_year(y) for y in calendar_years])
    n_grid         = len(years)

    for i in range(x.shape[0]):
        # Wall time spent on this design point, used later to measure the emulator speed-up
        t_start = time.perf_counter()

        # =========================
        # 1. Beam properties (durability analysis)
        # =========================
        base_fck = float(x[i][0])
        base_rh  = float(x[i][1])
        base_cov = float(x[i][2])

        # =========================
        # 2. Generate latent variables (humidity uncertainty)
        # =========================
        rh_latent, fck_latent, cov_latent = generate_latent_variables(n_latent_samples)

        # =========================
        # 3. Carbonation analysis for each latent humidity, fck and cover sample.
        # =========================
        new_rh_raw  = base_rh * rh_latent
        new_fck_raw = base_fck * fck_latent
        new_cov_raw = base_cov * cov_latent

        # Ensure physical limits
        new_rh  = np.clip(new_rh_raw, 0.0, 100.0)
        new_fck = np.clip(new_fck_raw, 0.0, None)
        new_cov = np.clip(new_cov_raw, 0.0, None)

        n_total  = n_latent_samples * n_grid
        batch_df = pd.DataFrame({
                                    't (years)':            np.tile(years, n_latent_samples),
                                    'CO2 (%)':              np.tile(co2_values, n_latent_samples),
                                    'fc (MPa)':             np.repeat(new_fck, n_grid),
                                    'RH (%)':               np.repeat(new_rh, n_grid),
                                    'Type of cement':       np.full(n_total, cement_type),
                                    'Exposure conditions':  np.full(n_total, exposure_conditions),
                                 })
        batch_df = batch_df[carb_model.feature_names_in_]

        depths = np.asarray(carb_model.predict(batch_df), dtype=float).reshape(n_latent_samples, n_grid)
        depths = np.maximum.accumulate(depths, axis=1)  # same effect as the per-sample cummax profile

        carbonation_depths = _interp_profile_at(calendar_years, depths, year_query)
        carbonation_depths = np.clip(carbonation_depths, 0.0, None)

        # =========================
        # 3.1. Emulator of state limit function g = cover - carbonation depth
        # =========================
        g_vals = new_cov - carbonation_depths  # g = cover - carbonation depth (failure if g < 0)

        # =========================
        # 4. Create DataFrame
        # =========================
        df = pd.DataFrame({
                            names_x_variables[0]: [x[i, 0]] * n_latent_samples,
                            names_x_variables[1]: [x[i, 1]] * n_latent_samples,
                            names_x_variables[2]: [x[i, 2]] * n_latent_samples,
                            'RH_latent': rh_latent,
                            'RH_effective': new_rh_raw,
                            'FCK_latent': fck_latent,
                            'FCK_effective': new_fck_raw,
                            'cov_latent': cov_latent,
                            'cov_effective': new_cov_raw,
                            'Carbonation_depth_mm': carbonation_depths,
                            'Time (years)': time_step,
                            'g': g_vals
                        })

        # =========================
        # 5. GLAM fitting
        # =========================
        if np.std(g_vals) < 1e-6:
            lambdas = [np.nan, np.nan, np.nan, np.nan]
        else:
            try:
                emulator = glam.GlamFKML()
                sol = emulator.fit_lambdas(df['g'].values, method="least_squares")
                if sol.status in [-1, -2]:
                    lambdas = [np.nan] * 4
                else:
                    lambdas = sol.x
            except Exception as e:
                if verbose:
                    print(f"  GLAM fitting failed: {e}")
                lambdas = [np.nan] * 4

        df['lambda 1'] = lambdas[0]
        df['lambda 2'] = lambdas[1]
        df['lambda 3'] = lambdas[2]
        df['lambda 4'] = lambdas[3]

        # Cost of producing this design point: latent sampling, carbonation batch and GLAM fitting
        df['Processing time (s)'] = time.perf_counter() - t_start

        dfs.append(df)

        if verbose:
            print(f"  Sample {i+1}:")
            print(f"    P(g < 0) = {np.mean(g_vals < 0):.4f}")
            print(f"    Mean carbonation depth = {np.mean(carbonation_depths):.2f} mm")

    df_full    = pd.concat(dfs, ignore_index=True)
    id_columns = list(names_x_variables[:3])
    df_unique  = (
                    df_full[id_columns + ['lambda 1', 'lambda 2', 'lambda 3', 'lambda 4', 'Processing time (s)']].drop_duplicates(subset=id_columns).reset_index(drop=True)
                 )

    return df_full, df_unique


def generate_dataset_at_time_durability(x_train: np.ndarray, x_val: np.ndarray, carb_model: Any, time_step: float, cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2, n_latent_samples: int = 1000, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Stage 1 of the split durability pipeline: run the emulator on the training and validation design samples at a single time step, and save both datasets to disk.

    This is the only stage that runs `carb_model.predict`, draws latent samples and fits the GLD — the expensive part that `Processing time (s)` measures. Splitting it from the PCE fit (`train_and_validate_pce_from_dataset_durability`) lets the dataset be generated once, in its own notebook, and the PCE refit or re-validated later without repeating any simulation.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<split>_<time_step>_install_<year>_cement_<type>_exposure_<exposure>.pkl` naming convention, where `<split>` is `train` or `val`.

    :param x_train: Design samples used to later train the PCE, shape (n_samples, 3) as [fck, rh, cover]
    :param x_val: Independent design samples used to later validate the PCE, shape (n_samples_validation, 3)
    :param carb_model: Trained ML model for carbonation depth prediction
    :param time_step: Time step of the analysis [years]
    :param cement_type: Type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
    :param installation_year: Calendar year of installation
    :param exposure_conditions: Exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected])
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each split

    :return: Dictionary with the full/unique dataframes for the train and validation splits, the total emulator wall time, and the paths written
    """

    out_dir     = Path(output_dir)
    tag         = f'{time_step}_install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}'
    emulator_kw = dict(names_x_variables=["fck", "rh", "cov"], carb_model=carb_model, cement_type=cement_type,
                       installation_year=installation_year, exposure_conditions=exposure_conditions,
                       time_step=time_step, n_latent_samples=n_latent_samples, verbose=False)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING DATASET FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    paths           = {}
    result          = {'time_step': time_step, 'paths': paths}
    emulator_time_s = 0.0
    for split, x in (('train', x_train), ('val', x_val)):
        df_full, df_unique = emulator_function_time_durability(x=x, **emulator_kw)
        result[f'df_full_{split}']   = df_full
        result[f'df_unique_{split}'] = df_unique
        emulator_time_s             += float(df_unique['Processing time (s)'].sum())

        if save:
            out_dir.mkdir(parents=True, exist_ok=True)
            for kind, frame in (('dataset_full', df_full), ('dataset_unique', df_unique)):
                key         = f'{kind}_{split}'
                paths[key]  = out_dir / f'{n_latent_samples}_{kind}_{split}_{tag}.pkl'
                with open(paths[key], 'wb') as f:
                    dill.dump(frame, f)

        if verbose:
            print(f'  {split}: {len(x)} design points, {df_unique["Processing time (s)"].sum():.2f} s total')

    result['emulator_time_s'] = emulator_time_s

    return result


def train_and_validate_pce_from_dataset_durability(df_unique_train: pd.DataFrame, df_unique_val: pd.DataFrame, joint: Any, time_step: float, installation_year: int = 1990, cement_type: int = 3, exposure_conditions: int = 2, n_latent_samples: int = 1000, n_lambdas: int = 4, max_degree: int = 3, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Stage 2 of the split durability pipeline: fit a PCE metamodel to a previously generated lambda dataset and validate it. Makes no emulator calls and draws no latent samples.

    Companion of `generate_dataset_at_time_durability`: takes its saved `dataset_unique` outputs (train and validation splits) and performs the PCE fit and scoring that `train_and_validate_pce_at_time` used to do inline with the data generation.

    Artefacts are written to `output_dir` with the same `<n_latent_samples>_<kind>_<time_step>_install_<year>_cement_<type>_exposure_<exposure>.pkl` naming convention as `train_and_validate_pce_at_time`, so downstream notebooks that only read the PCE metamodel don't need to change.

    :param df_unique_train: `dataset_unique_train` dataframe, as saved by `generate_dataset_at_time_durability`
    :param df_unique_val: `dataset_unique_val` dataframe, as saved by `generate_dataset_at_time_durability`
    :param joint: UQpy JointIndependent distribution of the design variables, used for the polynomial basis. Must match the one used to draw `df_unique_train`/`df_unique_val`
    :param time_step: Time step of the analysis (bookkeeping and filenames only — the time effect is already baked into the lambdas)
    :param installation_year: Calendar year of installation. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param cement_type: Type of cement. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param exposure_conditions: Exposure conditions. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param n_latent_samples: Number of latent samples used to generate the dataset. Only used for the filename prefix, to match `generate_dataset_at_time_durability`
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param max_degree: Maximum total degree of the polynomial basis
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the fitted PCE and the validation statistics
    """

    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'{time_step}_install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}'
    id_columns  = ['fck', 'rh', 'cov']

    if verbose:
        print(f'\n{"-"*40}')
        print(f'TRAINING PCE FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    # =========================
    # 1. PCE metamodel
    # =========================
    x_train           = df_unique_train[id_columns].to_numpy()
    y_train           = df_unique_train[lambda_cols].to_numpy()
    polynomial_basis  = TotalDegreeBasis(joint, max_degree)
    least_squares     = LeastSquareRegression()
    pce_metamodel     = PolynomialChaosExpansion(polynomial_basis=polynomial_basis, regression_method=least_squares)
    pce_metamodel.fit(x_train, y_train)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths['pce_metamodel'] = out_dir / f'{n_latent_samples}_pce_metamodel_{tag}.pkl'
        with open(paths['pce_metamodel'], 'wb') as f:
            dill.dump(pce_metamodel, f)
        if verbose:
            print('1. PCE training dataset has been saved!')

    # =========================
    # 2. Validation
    # =========================
    x_val          = df_unique_val[id_columns].to_numpy()
    y_val_true     = df_unique_val[lambda_cols].to_numpy()
    y_val_pred     = pce_metamodel.predict(x_val)

    mse_per_lambda = [mean_squared_error(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]
    r2_per_lambda  = [r2_score(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]

    stats_row = {f'MSE λ{i+1}': mse_per_lambda[i] for i in range(n_lambdas)}
    stats_row.update({f'R² λ{i+1}': r2_per_lambda[i] for i in range(n_lambdas)})
    statistics_ = pd.DataFrame(stats_row, index=[0])

    if save:
        paths['pce_validation_stats'] = out_dir / f'{n_latent_samples}_pce_validation_stats_{tag}.pkl'
        with open(paths['pce_validation_stats'], 'wb') as f:
            dill.dump(statistics_, f)
        if verbose:
            print('2. PCE statistcs has been saved!')

    return {
             'time_step':     time_step,
             'pce_metamodel': pce_metamodel,
             'statistics':    statistics_,
             'paths':         paths,
           }


# =============================================================================
# LEGACY / UNUSED — not called by any current *_final notebook, kept for reference
# =============================================================================

def carbonation_profile(model_: Any, lifetime: float, fc: float, rh: float, cement_type: int, exposure: int, start_year: int) -> pd.DataFrame:
    """Generate carbonation profile starting at a given calendar year.

    :param model_: trained ML model for carbonation depth prediction, which should have a method .predict() and an attribute .feature_names_in_ that contains the names of the features used for training.
    :param lifetime: Design life of the structure [years]
    :param fc: Concrete compressive strength [MPa]
    :param rh: Relative humidity [%]
    :param cement_type: Type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
    :param exposure: Exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected])
    :param start_year: Calendar year of installation

    :return: DataFrame with columns C02 concentration (%), compressive strength (MPa), relative humidity (%), type of cement, exposure conditions, year, and carbonation depth (mm)
    """

    # Time steps
    years = np.arange(0, lifetime + 1,10)

    # Romain calendar
    calendar_years = start_year + years

    # CO2 emission
    co2_values = [co2_percentage_year(y) for y in calendar_years]

    # Carbonation AI model and profile
    df      = pd.DataFrame({'t (years)': years, 'CO2 (%)': co2_values, 'fc (MPa)': [fc]*len(years), 'RH (%)': [rh]*len(years), 'Type of cement': [cement_type]*len(years), 'Exposure conditions': [exposure]*len(years)})
    df      = df[model_.feature_names_in_]
    depth   = model_.predict(df)
    profile = pd.DataFrame({'calendar year': calendar_years, 't (years)': years, 'CO2 (%)': co2_values, 'carbonation depth (mm)': depth})
    profile['carbonation depth (mm)'] = profile['carbonation depth (mm)'].cummax()

    return profile


def carbonation_depth_at_time(profile: pd.DataFrame, t_query: float) -> float:
    """Returns carbonation depth at a specific time.

    :param profile : DataFrame with columns ['calendar year', 'carbonation depth (mm)']
    :param t_query : Calendar year for which to query the carbonation depth

    :return: Carbonation depth at the specified calendar year
    """

    t     = profile['calendar year'].values
    depth = profile['carbonation depth (mm)'].values

    return float(np.interp(t_query, t, depth))


def train_and_validate_pce_at_time_benchmark(x_train: np.ndarray, joint: Any, time_step: float, n_latent_samples: int = 1000, n_samples_validation: int = 250, n_lambdas: int = 4, max_degree: int = 3, k_factor_final: float = 0.3, z1_std: float = 0.028, z2_std: float = 0.096, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Build the R/S benchmark dataset at a single time step, fit a PCE metamodel to the GLD lambdas, and validate it on a fresh sample.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<time_step>_benchmark.pkl` naming convention.

    :param x_train: Design samples used to train the PCE, shape (n_samples, 2) as [R, S]
    :param joint: UQpy JointIndependent distribution of R and S, used for the polynomial basis and to draw the validation samples
    :param time_step: Time step of the analysis, feeding the degradation factor k(t)
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param n_samples_validation: Number of independent samples drawn from `joint` to validate the PCE
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param max_degree: Maximum total degree of the polynomial basis
    :param k_factor_final: Value of the degradation factor at t = 100. Use 1.0 for no time effect
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the emulator dataframes, the fitted PCE, the validation statistics, the total emulator wall time, and the paths written
    """

    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'{time_step}_benchmark'
    emulator_kw = dict(names_x_variables=["r", "s"], time_step=time_step, n_latent_samples=n_latent_samples, k_factor_final=k_factor_final, z1_std=z1_std, z2_std=z2_std, verbose=False)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'PROCESSING EMULATOR FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    # =========================
    # 1. Emulator dataset (state limit function and lambdas)
    # =========================
    df_full, df_unique = emulator_function_time_benchmark(x=x_train, **emulator_kw)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        for kind, frame in (('dataset_full', df_full), ('dataset_unique', df_unique)):
            paths[kind] = out_dir / f'{n_latent_samples}_{kind}_{tag}.pkl'
            with open(paths[kind], 'wb') as f:
                dill.dump(frame, f)
        if verbose:
            print('1. The dataset has been saved!')

    # =========================
    # 2. PCE metamodel
    # =========================
    y_train          = df_unique[lambda_cols].to_numpy()
    polynomial_basis = TotalDegreeBasis(joint, max_degree)
    least_squares    = LeastSquareRegression()
    pce_metamodel    = PolynomialChaosExpansion(polynomial_basis=polynomial_basis, regression_method=least_squares)
    pce_metamodel.fit(x_train, y_train)

    if save:
        paths['pce_metamodel'] = out_dir / f'{n_latent_samples}_pce_metamodel_{tag}.pkl'
        with open(paths['pce_metamodel'], 'wb') as f:
            dill.dump(pce_metamodel, f)
        if verbose:
            print('2. PCE training dataset has been saved!')

    # =========================
    # 3. Validation on an independent sample
    # =========================
    x_val                      = joint.rvs(n_samples_validation)
    df_full_val, df_unique_val = emulator_function_time_benchmark(x=x_val, **emulator_kw)
    y_val_true                 = df_unique_val[lambda_cols].to_numpy()
    y_val_pred                 = pce_metamodel.predict(x_val)

    mse_per_lambda = [mean_squared_error(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]
    r2_per_lambda  = [r2_score(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]

    stats_row = {f'MSE λ{i+1}': mse_per_lambda[i] for i in range(n_lambdas)}
    stats_row.update({f'R² λ{i+1}': r2_per_lambda[i] for i in range(n_lambdas)})
    statistics_ = pd.DataFrame(stats_row, index=[0])

    if save:
        paths['pce_validation_stats'] = out_dir / f'{n_latent_samples}_pce_validation_stats_{tag}.pkl'
        with open(paths['pce_validation_stats'], 'wb') as f:
            dill.dump(statistics_, f)
        if verbose:
            print('3. PCE statistcs has been saved!')

    return {
             'time_step':       time_step,
             'df_full':         df_full,
             'df_unique':       df_unique,
             'pce_metamodel':   pce_metamodel,
             'statistics':      statistics_,
             'df_full_val':     df_full_val,
             'df_unique_val':   df_unique_val,
             'emulator_time_s': float(df_unique['Processing time (s)'].sum()),
             'paths':           paths,
           }


def train_and_validate_pce_at_time(x_train: np.ndarray, joint: Any, carb_model: Any, time_step: float, cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2, n_latent_samples: int = 1000, n_samples_validation: int = 250, n_lambdas: int = 4, max_degree: int = 3, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Build the durability emulator dataset at a single time step, fit a PCE metamodel to the GLD lambdas, and validate it on a fresh sample.

    Runs the three stages of one time step of the dataset pipeline: (1) evaluates `emulator_function_time_durability` on the design samples to obtain the lambdas, (2) fits a PCE of `max_degree` mapping design variables to lambdas, and (3) re-evaluates the emulator on an independent validation sample to score the PCE with MSE and R2 per lambda.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<time_step>_install_<year>_cement_<type>_exposure_<exposure>.pkl` naming convention, which is what the downstream notebooks expect.

    :param x_train: Design samples used to train the PCE, shape (n_samples, 3) as [fck, rh, cover]
    :param joint: UQpy JointIndependent distribution of the design variables, used for the polynomial basis and to draw the validation samples
    :param carb_model: Trained ML model for carbonation depth prediction
    :param time_step: Time step of the analysis [years]
    :param cement_type: Type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
    :param installation_year: Calendar year of installation
    :param exposure_conditions: Exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected])
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param n_samples_validation: Number of independent samples drawn from `joint` to validate the PCE
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param max_degree: Maximum total degree of the polynomial basis
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the emulator dataframes, the fitted PCE, the validation statistics, and the paths written
    """

    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'{time_step}_install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}'
    emulator_kw = dict(names_x_variables=["fck", "rh", "cov"], carb_model=carb_model, cement_type=cement_type,
                       installation_year=installation_year, exposure_conditions=exposure_conditions,
                       time_step=time_step, n_latent_samples=n_latent_samples, verbose=False)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'PROCESSING EMULATOR FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    # =========================
    # 1. Emulator dataset (carbonation depth and lambdas)
    # =========================
    df_full, df_unique = emulator_function_time_durability(x=x_train, **emulator_kw)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        for kind, frame in (('dataset_full', df_full), ('dataset_unique', df_unique)):
            paths[kind] = out_dir / f'{n_latent_samples}_{kind}_{tag}.pkl'
            with open(paths[kind], 'wb') as f:
                dill.dump(frame, f)
        if verbose:
            print('1. The dataset has been saved!')

    # =========================
    # 2. PCE metamodel
    # =========================
    y_train          = df_unique[lambda_cols].to_numpy()
    polynomial_basis = TotalDegreeBasis(joint, max_degree)
    least_squares    = LeastSquareRegression()
    pce_metamodel    = PolynomialChaosExpansion(polynomial_basis=polynomial_basis, regression_method=least_squares)
    pce_metamodel.fit(x_train, y_train)

    if save:
        paths['pce_metamodel'] = out_dir / f'{n_latent_samples}_pce_metamodel_{tag}.pkl'
        with open(paths['pce_metamodel'], 'wb') as f:
            dill.dump(pce_metamodel, f)
        if verbose:
            print('2. PCE training dataset has been saved!')

    # =========================
    # 3. Validation on an independent sample
    # =========================
    x_val                      = joint.rvs(n_samples_validation)
    df_full_val, df_unique_val = emulator_function_time_durability(x=x_val, **emulator_kw)
    y_val_true                 = df_unique_val[lambda_cols].to_numpy()
    y_val_pred                 = pce_metamodel.predict(x_val)

    mse_per_lambda = [mean_squared_error(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]
    r2_per_lambda  = [r2_score(y_val_true[:, i], y_val_pred[:, i]) for i in range(n_lambdas)]

    stats_row = {f'MSE λ{i+1}': mse_per_lambda[i] for i in range(n_lambdas)}
    stats_row.update({f'R² λ{i+1}': r2_per_lambda[i] for i in range(n_lambdas)})
    statistics_ = pd.DataFrame(stats_row, index=[0])

    if save:
        paths['pce_validation_stats'] = out_dir / f'{n_latent_samples}_pce_validation_stats_{tag}.pkl'
        with open(paths['pce_validation_stats'], 'wb') as f:
            dill.dump(statistics_, f)
        if verbose:
            print('3. PCE statistcs has been saved!')

    return {
             'time_step':       time_step,
             'df_full':         df_full,
             'df_unique':       df_unique,
             'pce_metamodel':   pce_metamodel,
             'statistics':      statistics_,
             'df_full_val':     df_full_val,
             'df_unique_val':   df_unique_val,
             'emulator_time_s': float(df_unique['Processing time (s)'].sum()),
             'paths':           paths,
           }


# if __name__ == "__main__":
#     name_best_model = r'D:\github\2024-1_victor_hugo_renata_maria\beam_problem_1\model_NeuralNetwork_MLP_fold_4.pkl'
#     # Load the model
#     model = joblib.load(name_best_model)
#     print("Carbonation model loaded successfully!")
#     print(f"   Expected features: {model.feature_names_in_}")
#     # Example usage
#     x_pce_rvs = np.array([[30, 40, 30], [35, 40, 28]])
#     cement_type          = 3
#     installation_year    = 1990
#     exposure_conditions  = 2
#     n_samples            = 50          # Number of design samples. Use 1 for testing one sample
#     n_latent_samples     = 500        # Number of latent samples per design sample
#     n_samples_validation = 3           # Number of validation samples
#     n_lambdas            = 4           # Number of λs to be predicted (λ1, λ2, λ3, λ4)
#     times = [10]
#     for t in times:
#         # ============================================================
#         # EMULATOR FUNCTION - CARBONATION DEPTH AND LAMBDAS
#         # ============================================================
#         df_full, df_unique = emulator_function_time_durability(
#                                                     x=x_pce_rvs,
#                                                     names_x_variables=["fck", "rh", "cov"],
#                                                     carb_model=model,
#                                                     cement_type=cement_type,
#                                                     installation_year=installation_year,
#                                                     exposure_conditions=exposure_conditions,
#                                                     time_step=t,
#                                                     n_latent_samples=n_latent_samples,
#                                                     verbose=False
#                                                 )
#         print(df_unique.head())
#         print(df_full.describe())