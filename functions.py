import os
import time
from pathlib import Path
from functools import lru_cache
from numbers import Real

import numpy as np
import pandas as pd
from typing import Optional, Any
import seaborn as sns
import pickle
import dill
from scipy.integrate import odeint, simpson
from scipy.stats import ks_2samp, wasserstein_distance
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


def emulator_function_time_benchmark(x: np.ndarray, names_x_variables: list, time_step: float = 0.0, n_latent_samples: int = 1000, k_factor_final: float = 0.3, t_final: float = 100.0, z1_std: float = 0.028, z2_std: float = 0.096, n_starts: int = 15, seed: int = 42, verbose: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    r"""Compute the emulator of the R/S benchmark state limit function.

    The state limit function is

    .. math::

        g = k(t) \cdot \frac{R}{z_1} - S \cdot z_2

    where :math:`R` is the resistance, :math:`S` is the load, and :math:`z_1` and :math:`z_2` are
    normal latent multipliers. Failure is :math:`g < 0`.

    The degradation factor

    .. math::

        k(t) = 1 + (k_{final} - 1) \, \frac{t}{100}

    shrinks the resistance linearly with time, reaching ``k_factor_final`` at :math:`t = t_{final}`
    and **holding it there** for :math:`t > t_{final}`. The clamp is not cosmetic: without it the
    factor keeps falling past ``k_factor_final`` and crosses zero at
    :math:`t = t_{final}/(1 - k_{final})`, which flips the sign of the resistance and produces
    degenerate response distributions that no GLD can fit (lambda_2 comes back negative).
    Setting ``k_factor_final`` to 1.0 removes the time effect and leaves the plain
    :math:`g = R/z_1 - S z_2`.

    :param x: Design samples, shape (n_samples, 2) as [R, S]
    :param names_x_variables: Names of the two design variables, used as the identifying columns of the output
    :param time_step: Time step of the analysis, feeding the degradation factor k(t)
    :param n_latent_samples: Number of latent samples per design sample
    :param k_factor_final: Value of the degradation factor at t = t_final, held constant afterwards. Use 1.0 for no time effect
    :param t_final: Time at which the degradation factor reaches k_factor_final (years)
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier
    :param n_starts: Number of pyGLAM multi-start attempts per GLAM fit; each restart begins from a
        different point on the shape plane, which guards against the moment-matching optimizer
        settling in a poor local minimum (the failure mode that produced bad lambda 2 fits)
    :param seed: Seed used by pyGLAM to draw extra multi-start points once `n_starts` exceeds its
        fixed shape grid, for reproducible fits
    :param verbose: Whether to print per-sample diagnostics

    :return: [0] = one row per latent replica ; [1] = one row per design point, with the lambdas and the processing time
    """

    dfs = []

    # =========================
    # 0. Degradation factor
    # =========================
    k_factor = k_factor_final if time_step >= t_final else 1 + (k_factor_final - 1) * time_step / t_final

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
                sol = emulator.fit_lambdas(df['g'].values, method="least_squares", n_starts=n_starts, seed=seed)
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


def generate_dataset_at_time_benchmark(x_train: np.ndarray, x_val: np.ndarray, time_step: float, n_latent_samples: int = 1000, k_factor_final: float = 0.3, t_final: float = 100.0, z1_std: float = 0.028, z2_std: float = 0.096, n_starts: int = 15, seed: int = 42, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Run the emulator on the training and validation design samples at a single time step, and save both datasets to disk.

    This is the only stage that draws latent samples and fits the GLD — the expensive part that `Processing time (s)` measures. Splitting it from the PCE fit (`train_and_validate_pce_from_dataset_benchmark`) lets the dataset be generated once, in its own notebook, and the PCE refit or re-validated later without repeating any simulation.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<split>_<time_step>_benchmark.pkl` naming convention, where `<split>` is `train` or `val`.

    :param x_train: Design samples used to later train the PCE, shape (n_samples, 2) as [R, S]
    :param x_val: Independent design samples used to later validate the PCE, shape (n_samples_validation, 2)
    :param time_step: Time step of the analysis, feeding the degradation factor k(t)
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param k_factor_final: Value of the degradation factor at t = t_final, held constant afterwards. Use 1.0 for no time effect
    :param t_final: Time at which the degradation factor reaches k_factor_final (years)
    :param z1_std: Standard deviation of the resistance latent multiplier
    :param z2_std: Standard deviation of the load latent multiplier
    :param n_starts: Number of pyGLAM multi-start attempts per GLAM fit, passed through to
        `emulator_function_time_benchmark`
    :param seed: Seed used by pyGLAM's multi-start, passed through to `emulator_function_time_benchmark`
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each split

    :return: Dictionary with the full/unique dataframes for the train and validation splits, the total emulator wall time, and the paths written
    """

    out_dir     = Path(output_dir)
    tag         = f'{time_step}_benchmark'
    emulator_kw = dict(names_x_variables=["r", "s"], time_step=time_step, n_latent_samples=n_latent_samples, k_factor_final=k_factor_final, t_final=t_final, z1_std=z1_std, z2_std=z2_std, n_starts=n_starts, seed=seed, verbose=False)

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


def _compare_gld_to_raw_benchmark(g_real: np.ndarray, lambda_pred: np.ndarray, n_grid: int = 400, random_state: int | np.random.Generator | None = 42) -> dict:
    r"""Score a predicted GLD directly against the raw Monte Carlo :math:`g` samples.

    Shared numerical core of `validate_pce_kl_divergence_benchmark` and
    `validate_nn_kl_divergence_benchmark`. The reference side is the raw data itself, not a GLD
    fitted to it, so the score measures only the surrogate's error and does not fold in the
    GLD-fitting error of pyGLAM on top of it. The predicted side is a fresh sample drawn from the
    surrogate's GLD, and `pyglam.Performance` does the scoring: it estimates a Gaussian KDE of each
    sample on a shared grid spanning the raw data's own range, integrates the KL divergence and
    :math:`R^2` over it, and computes the KS / Wasserstein / percentile diagnostics from the two
    samples directly.

    Both sides therefore go through the same KDE. If the predicted GLD puts almost no probability
    where the real data lives, its density is floored at `Performance`'s `eps` there, which makes the
    KL divergence large — that is the intended reading.

    A surrogate can also predict :math:`\lambda_2 \le 0`, which is not a valid GLD at all (the
    quantile function stops being increasing). That happens at a handful of extreme design points at
    late ages. Those are handed to `Performance` as an empty predicted sample, so they come back as
    NaN instead of raising: a sweep over the whole dataset still completes and the failures show up
    as gaps in the maps.

    :param g_real: Raw Monte Carlo g samples for one design point
    :param lambda_pred: The GLD being scored (lambda 1-4, in order)
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param random_state: Seed, NumPy Generator or None passed to pyGLAM's `rvs`. pyGLAM's `rvs`
        draws true random samples, so a fixed seed (the default) keeps this diagnostic reproducible;
        pass a shared `np.random.Generator` to draw a different sample per call while keeping a whole
        sweep reproducible from one seed

    :return: Dictionary with the KL divergence, KS statistic and p-value, Wasserstein distance, R² between the two densities, relative errors at P5/P50/P95, the shared grid, both densities, and the fresh sample drawn from the predicted GLD
    """

    g_real = np.asarray(g_real, dtype=float)
    g_pred = glam.GlamFKML(*lambda_pred).rvs(size=len(g_real), random_state=random_state) if float(lambda_pred[1]) > 0.0 else np.array([])

    result                   = glam.Performance(n_grid=n_grid).performance(g_real, g_pred)
    result['pdf_real']       = result.pop('pdf_true')
    result['g_pred_samples'] = g_pred

    return result


def validate_pce_kl_divergence_benchmark(pce_metamodel: Any, r: float, s: float, g_real: np.ndarray, lambda3: float, lambda4: float, n_grid: int = 400, random_state: int | np.random.Generator | None = 42) -> dict:
    r"""Score the PCE's predicted GLD against the raw Monte Carlo :math:`g` data, at one (R, S) design point.

    The PCE supplies lambda 1 / lambda 2 for :math:`(R, S)`; lambda 3 / lambda 4 are supplied by the
    caller. The PCE does predict all four, but its lambda 3 / lambda 4 are consistently poor (R² near
    zero or negative at every time step in `02_train_pce.ipynb`'s validation table), so they are
    written by hand instead — see `generate_rul_dataset_benchmark`, which fixes them the same way.

    The comparison is against `g_real` itself (via a KDE), not against a GLD fitted to it, so the
    score reflects the PCE's error alone and not pyGLAM's fitting error stacked on top. See
    `_compare_gld_to_raw_benchmark` for the metrics computed.

    :param pce_metamodel: Fitted PCE for the time step `g_real` was computed at, as returned by `train_and_validate_pce_from_dataset_benchmark`
    :param r: Resistance value of the design point being checked
    :param s: Load value of the design point being checked
    :param g_real: Raw Monte Carlo g samples for this design point (that design point's rows of `dataset_full`'s `g` column)
    :param lambda3: Fixed lambda 3 to pair with the PCE's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the PCE's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param random_state: Seed, NumPy Generator or None passed to pyGLAM's `rvs` for the fresh sample; see `_compare_gld_to_raw_benchmark`

    :return: Dictionary with the KL divergence, KS statistic, Wasserstein distance, R² between the two densities, relative errors at P5/P50/P95, the lambda vector used (plus the PCE's raw, unmodified prediction), the shared grid, both densities, and the fresh sample drawn from the PCE's GLD
    """

    lambda_pce_raw = np.asarray(pce_metamodel.predict(np.array([[r, s]]))[0], dtype=float)
    lambda_pce     = np.array([lambda_pce_raw[0], lambda_pce_raw[1], lambda3, lambda4], dtype=float)

    result = _compare_gld_to_raw_benchmark(g_real, lambda_pce, n_grid=n_grid, random_state=random_state)
    result['lambda_pce']     = lambda_pce
    result['lambda_pce_raw'] = lambda_pce_raw
    result['pdf_pce']        = result.pop('pdf_pred')
    result['g_pce_samples']  = result.pop('g_pred_samples')

    return result


def validate_nn_kl_divergence_benchmark(models: dict, scaler: Any, r: float, s: float, t: float, g_real: np.ndarray, lambda3: float, lambda4: float, n_grid: int = 400, random_state: int | np.random.Generator | None = 42) -> dict:
    r"""Score the global NN's predicted GLD against the raw Monte Carlo :math:`g` data, at one (R, S, t) design point.

    Mirrors `validate_pce_kl_divergence_benchmark`, for the global NN
    (`train_and_validate_nn_lambda_benchmark`) instead of the per-time-step PCE — same idea, but the
    NN takes :math:`t` directly, instead of needing one PCE per time step. The NN only ever predicts
    lambda 1 / lambda 2 by design, so lambda 3 / lambda 4 come from the caller here too.

    :param models: ``{'lambda 1': fitted MLPRegressor, 'lambda 2': fitted MLPRegressor}``, as returned by `train_and_validate_nn_lambda_benchmark`
    :param scaler: The fitted `StandardScaler` for `(r, s, t)`, as returned by `train_and_validate_nn_lambda_benchmark`
    :param r: Resistance value of the design point being checked
    :param s: Load value of the design point being checked
    :param t: Time step of the design point being checked
    :param g_real: Raw Monte Carlo g samples for this design point (that design point's rows of `dataset_full`'s `g` column)
    :param lambda3: Fixed lambda 3 to pair with the NN's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the NN's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param random_state: Seed, NumPy Generator or None passed to pyGLAM's `rvs` for the fresh sample; see `_compare_gld_to_raw_benchmark`

    :return: Dictionary with the KL divergence, KS statistic, Wasserstein distance, R² between the two densities, relative errors at P5/P50/P95, the lambda vector used, the shared grid, both densities, and the fresh sample drawn from the NN's GLD
    """

    x_scaled  = scaler.transform(np.array([[r, s, t]]))
    lambda_nn = np.array([float(models['lambda 1'].predict(x_scaled)[0]),
                          float(models['lambda 2'].predict(x_scaled)[0]),
                          lambda3,
                          lambda4], dtype=float)

    result = _compare_gld_to_raw_benchmark(g_real, lambda_nn, n_grid=n_grid, random_state=random_state)
    result['lambda_nn']    = lambda_nn
    result['pdf_nn']       = result.pop('pdf_pred')
    result['g_nn_samples'] = result.pop('g_pred_samples')

    return result


def validate_pce_kl_divergence_dataset_benchmark(pce_metamodel: Any, df_full: pd.DataFrame, time_step: float, lambda3: float, lambda4: float, n_grid: int = 400, max_points: int | None = None, random_state: int = 42, verbose: bool = True) -> pd.DataFrame:
    r"""Run `validate_pce_kl_divergence_benchmark` over every design point of one time step's `dataset_full`.

    Groups `df_full` by design point, pulls that point's raw Monte Carlo :math:`g` samples, and scores
    the PCE's predicted GLD against them — one row of statistics per design point. Stacking the
    result over every time step gives the (R, S) maps of surrogate error that
    `02_train_pce_plot.ipynb` plots.

    :param pce_metamodel: Fitted PCE for `time_step`, as returned by `train_and_validate_pce_from_dataset_benchmark`
    :param df_full: That time step's `dataset_full` frame, one row per latent replica
    :param time_step: Time step being scored [years], copied into the output frame
    :param lambda3: Fixed lambda 3 to pair with the PCE's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the PCE's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param max_points: Score only `max_points` design points, drawn at random from the ones present.
        None scores all of them. Scoring one point costs roughly 45 ms at `n_latent_samples=2500` and
        `n_grid=400`, so a full 2000-point sweep runs for about a minute and a half per time step;
        `max_points=10` turns that into a fraction of a second, for a thinned-out map to iterate on
    :param random_state: Seed for the whole sweep. A single `np.random.Generator` is seeded once from
        it, draws the `max_points` subsample, and is then advanced across the sweep, so each design
        point gets an independent pyGLAM draw while the whole sweep stays reproducible from one seed
    :param verbose: Whether to print progress

    :return: One row per design point, with `r`, `s`, `Time (years)` and the seven statistics
    """

    rng     = np.random.default_rng(random_state)
    grouped = list(df_full.groupby(['r', 's'], sort=False))

    # Thin the sweep at random rather than by taking the first rows: the design points are drawn
    # i.i.d., so the two coincide today, but a subsample keeps meaning "a smaller version of the same
    # map" if `df_full` ever arrives sorted or on a grid. Kept in dataset order for a readable frame.
    if max_points is not None and max_points < len(grouped):
        grouped = [grouped[i] for i in np.sort(rng.choice(len(grouped), size=max_points, replace=False))]

    if verbose:
        print(f'  t = {time_step:.2f} years: scoring {len(grouped)} design points')

    rows = []
    for (r, s), group in grouped:
        stats_ = validate_pce_kl_divergence_benchmark(
                                                         pce_metamodel=pce_metamodel,
                                                         r=r,
                                                         s=s,
                                                         g_real=group['g'].to_numpy(),
                                                         lambda3=lambda3,
                                                         lambda4=lambda4,
                                                         n_grid=n_grid,
                                                         random_state=rng,
                                                     )
        rows.append({
                        'r':             r,
                        's':             s,
                        'Time (years)':  time_step,
                        'KL':            stats_['kl_divergence'],
                        'KS':            stats_['ks_statistic'],
                        'Wasserstein':   stats_['wasserstein'],
                        'R2 (PDF)':      stats_['r2_pdf'],
                        'Rel. error P5':  stats_['rel_err_p5'],
                        'Rel. error P50': stats_['rel_err_p50'],
                        'Rel. error P95': stats_['rel_err_p95'],
                    })

    df_out    = pd.DataFrame(rows)
    n_invalid = int(df_out['KL'].isna().sum())
    if verbose and n_invalid:
        print(f'    {n_invalid} design point(s) scored NaN — the PCE predicted an invalid GLD (lambda 2 <= 0) there')

    return df_out


def generate_nn_dataset_benchmark(pce_metamodels: list, times: np.ndarray, joint: Any, n_points: int = 5000, n_lambdas: int = 4, lambda3_fixed: float | None = None, lambda4_fixed: float | None = None, n_latent_samples: int = 1000, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Build the (R, S, t) -> lambda dataset used to train a single global NN surrogate, by querying the per-time-step PCE metamodels instead of re-running the stochastic emulator.

    Companion of `train_and_validate_pce_from_dataset_benchmark`: reuses its fitted `pce_metamodel` (one per time step, already fit and validated against the emulator) as a cheap oracle — `pce_metamodel.predict(x)` costs microseconds, versus the emulator's per-point GLAM fit over `n_latent_samples` draws. That lets `n_points` be drawn far denser than the emulator dataset each PCE was itself trained on, at no extra Monte Carlo cost. This distills the `len(times)` separate per-time-step PCEs into training data for a single, continuous-in-t model.

    Artefacts are written to `output_dir` as `<n_latent_samples>_dataset_nn_benchmark.pkl`.

    :param pce_metamodels: Fitted `PolynomialChaosExpansion` models, one per entry of `times`, in the same order (as saved by `train_and_validate_pce_from_dataset_benchmark`)
    :param times: Time steps to stack into the dataset [years], paired positionally with `pce_metamodels`
    :param joint: UQpy JointIndependent distribution of R and S, used to draw the query points fed to each PCE
    :param n_points: Number of (R, S) query points drawn per time step
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param lambda3_fixed: If given, overrides the PCE's predicted `lambda 3` column with this fixed value for every row (the PCE's own lambda 3 / lambda 4 fits are consistently poor, see `validate_pce_kl_divergence_benchmark`). If None, keeps the PCE prediction
    :param lambda4_fixed: If given, overrides the PCE's predicted `lambda 4` column with this fixed value for every row. If None, keeps the PCE prediction
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
        if lambda3_fixed is not None:
            print(f'  lambda 3 fixed at {lambda3_fixed:.4f}')
        if lambda4_fixed is not None:
            print(f'  lambda 4 fixed at {lambda4_fixed:.4f}')

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
        if lambda3_fixed is not None and 'lambda 3' in lambda_cols:
            df['lambda 3'] = lambda3_fixed
        if lambda4_fixed is not None and 'lambda 4' in lambda_cols:
            df['lambda 4'] = lambda4_fixed
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


def generate_rul_dataset_benchmark(r: float, s: float, times: np.ndarray, n_latent_samples: int = 1000, lambda3_fixed: float | None = None, lambda4_fixed: float | None = None, n_glam_samples: int = 10000, random_state: int = 42, input_dir: str | Path = '.', output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
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
    :param random_state: Seed passed unchanged to `GlamFKML.rvs` at every time step. An integer seed
        makes `rvs` reseed a fresh generator on every call, so the same integer reproduces the same
        underlying uniform draws at each time step, making every row of `samples` a genuine sample
        path rather than independent draws per column
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
    # Sampled via GlamFKML.rvs, with the SAME `random_state` passed at every time step — NOT one
    # independent draw per time step. `GlamFKML.rvs` reseeds a fresh generator from an integer seed on
    # every call, so passing the same integer here reproduces the identical underlying uniform draws
    # at each time step, exactly as if a single uniform vector had been reused across columns.
    # The rows of `samples` are read downstream as sample *paths*: `compute_rul_benchmark` walks each
    # row looking for the first down-crossing, which only means anything if the row is a trajectory.
    # Drawing each column independently destroys the dependence across time and leaves roughly 90% of
    # the rows non-monotonic, which is impossible for a monotonically degrading process and biases the
    # time-to-threshold towards later, non-conservative values.
    #
    # Holding the quantile level fixed makes every path comonotonic, hence monotonic whenever the
    # marginals shift monotonically in time. Checked against the analytical benchmark (paths built by
    # freezing z1 and z2 instead), this construction reproduces the reference mean and P5 of the
    # time-to-threshold to within 0.1 year. `quantile_trim=0.0` keeps the tails: `rvs` trims 0.1% from
    # each tail by default, which would otherwise censor exactly the extreme behaviour this benchmark
    # is meant to capture.
    samples = np.empty((n_glam_samples, len(times)))
    for i, row in lambda_df.iterrows():
        model         = glam.GlamFKML(row['lambda 1'], row['lambda 2'], row['lambda 3'], row['lambda 4'])
        samples[:, i] = model.rvs(size=n_glam_samples, quantile_trim=0.0, random_state=random_state)
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

CO2_SCENARIOS = ("SSP1-2.6", "SSP2-4.5", "SSP5-8.5")


def _co2_scenario_name(scenario: str) -> str:
    """Accept canonical SSP names or compact names such as ``ssp245``."""
    if isinstance(scenario, str):
        key = scenario.strip().upper().replace("-", "").replace(".", "")
        for name in CO2_SCENARIOS:
            if key == name.replace("-", "").replace(".", ""):
                return name
    raise ValueError(f"Unknown CO2 scenario {scenario!r}. Choose one of {CO2_SCENARIOS}.")


@lru_cache(maxsize=1)
def _co2_concentrations() -> pd.DataFrame:
    """Read the versioned annual table once, independently of the working directory."""
    return pd.read_csv(Path(__file__).resolve().parent / "data/co2/co2_concentrations_1900_2100.csv")


def co2_percentage_year(year: float, scenario: str = "SSP2-4.5") -> float:
    """Return annual global atmospheric CO2 concentration in percent (ppm / 10000).

    Uses the CMIP6 historical series through 2014 and published SSP concentrations
    from 2015 through 2100 (Meinshausen et al., 2017 and 2020). All scenarios share
    the historical period. Fractional years are linearly interpolated between
    annual values; years outside the available range raise ``ValueError``.
    This is atmospheric concentration, not carbon consumption or CO2 emissions.

    :param year: Calendar year between 1900 and 2100, inclusive
    :param scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5;
        compact names such as ``ssp245`` are also accepted
    :return: CO2 concentration in percent, e.g. about 0.0602782 for 2100 / SSP2-4.5

    Example::

        co2 = co2_percentage_year(2050, "SSP2-4.5")  # about 0.0506875 (%)
    """
    scenario = _co2_scenario_name(scenario)
    if isinstance(year, (bool, np.bool_)) or not isinstance(year, Real) or not np.isfinite(year) or not 1900 <= year <= 2100:
        raise ValueError("Year must be a finite number between 1900 and 2100 (inclusive).")
    data = _co2_concentrations()
    return float(np.interp(year, data["year"], data[scenario]) / 10000.0)


# Possan et al. (2016) carbonation model coefficients, Table 3a — one entry per cement type,
# keyed by the `cement_type` encoding used throughout this pipeline.
POSSAN_CEMENT_COEFFICIENTS = {
                                 0: {'name': 'CP II Z',  'k_c': 23.66, 'k_fc': 1.50, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 1: {'name': 'CP V-ARI', 'k_c': 19.80, 'k_fc': 1.70, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1300.0},
                                 2: {'name': 'CP IV',    'k_c': 33.27, 'k_fc': 1.70, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1000.0},
                                 3: {'name': 'CP II F',  'k_c': 21.68, 'k_fc': 1.50, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1100.0},
                                 4: {'name': 'CP III',   'k_c': 30.50, 'k_fc': 1.70, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 5: {'name': 'CP II E',  'k_c': 22.48, 'k_fc': 1.50, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 6: {'name': 'CP I',     'k_c': 19.80, 'k_fc': 1.70, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1300.0},
                             }

# Possan et al. (2016) carbonation model coefficients, Table 3b — exposure condition factor,
# keyed by the `exposure_conditions` encoding used throughout this pipeline.
POSSAN_EXPOSURE_COEFFICIENTS = {
                                   0: {'name': 'PIA — internal, protected from rain', 'k_ce': 1.30},
                                   1: {'name': 'UEA — external, exposed to rain',     'k_ce': 0.65},
                                   2: {'name': 'PEA — external, protected from rain', 'k_ce': 1.00},
                               }


def possan_coefficients(cement_type: int = 3, exposure_conditions: int = 2) -> dict:
    """Looks up the six Possan et al. (2016) model coefficients for a given cement type and exposure condition, combining Tables 3a and 3b.

    :param cement_type: Type of cement (0: CP II Z, 1: CP V-ARI, 2: CP IV, 3: CP II F, 4: CP III, 5: CP II E, 6: CP I)
    :param exposure_conditions: Exposure conditions (0: PIA internal protected, 1: UEA external unprotected, 2: PEA external protected)

    :return: Dictionary with the coefficients k_c, k_fc, k_ad, k_co_2, k_rh and k_ce, plus the descriptive names
    """

    if cement_type not in POSSAN_CEMENT_COEFFICIENTS:
        raise ValueError(f"Unknown cement_type {cement_type}. Valid values: {sorted(POSSAN_CEMENT_COEFFICIENTS)}")
    if exposure_conditions not in POSSAN_EXPOSURE_COEFFICIENTS:
        raise ValueError(f"Unknown exposure_conditions {exposure_conditions}. Valid values: {sorted(POSSAN_EXPOSURE_COEFFICIENTS)}")

    cement   = POSSAN_CEMENT_COEFFICIENTS[cement_type]
    exposure = POSSAN_EXPOSURE_COEFFICIENTS[exposure_conditions]

    return {
               'k_c':           cement['k_c'],
               'k_fc':          cement['k_fc'],
               'k_ad':          cement['k_ad'],
               'k_co_2':        cement['k_co_2'],
               'k_rh':          cement['k_rh'],
               'k_ce':          exposure['k_ce'],
               'cement_name':   cement['name'],
               'exposure_name': exposure['name'],
           }


def carbonation_depth_possan(f_ck: np.ndarray | float, t: np.ndarray | float, ur: np.ndarray | float, co_2: np.ndarray | float, k_c: float, k_fc: float, k_ad: float, k_co_2: float, k_rh: float, k_ce: float, ad: np.ndarray | float = 0.0) -> np.ndarray | float:
    r"""Carbonation depth of concrete according to the model of Possan et al. (2016), https://doi.org/10.1007/s41024-016-0010-9.

    .. math::

        y(t) = k_c \left(\frac{20}{f_{ck}}\right)^{k_{fc}} \left(\frac{t}{20}\right)^{1/2}
               \exp\left[\frac{k_{ad}\,ad^{3/2}}{40 + f_{ck}}
                       + \frac{k_{CO_2}\sqrt{CO_2}}{60 + f_{ck}}
                       - \frac{k_{UR}(UR - 0.58)^2}{100 + f_{ck}}\right] k_{ce}

    Fully vectorized: every physical argument accepts a scalar or a numpy array, and broadcasting
    rules apply. This is the closed-form simulator of the durability pipeline — it replaces the
    surrogate ML model used previously, so the emulator is trained against the mechanistic model
    itself rather than against an approximation of it.

    Unit conventions, which differ from the original single-point implementation:

    - the result is returned in **millimetres**, matching the concrete cover used elsewhere in this
      pipeline (`g = cover - carbonation depth` is therefore a mm - mm difference);
    - `ur` is a **fraction** in [0, 1] (0.70 for 70% RH), not a percentage. The quadratic term peaks
      at UR = 0.58, i.e. carbonation is fastest around 58% relative humidity. Passing a percentage
      here silently produces a meaningless depth, so values above 1.5 raise.

    The caller is responsible for keeping `f_ck` strictly positive and `ur` within physical bounds
    after any latent perturbation, as `emulator_function_time_durability` already does by clipping.

    .. note::

        The synthetic dataset behind the previously used ML surrogate was generated with
        ``ad = 10`` (%). Calling this function with the default ``ad = 0`` reproduces neither that
        dataset nor the earlier durability results: depths come out roughly 1.6 mm shallower.
        Pass ``ad=10.0`` to stay consistent with the existing pipeline. Checked against the
        surrogate over the full input box: bias +0.05 mm, standard deviation 0.30 mm,
        R2 = 0.999 at ``ad = 10``, against bias +1.64 mm and R2 = 0.978 at ``ad = 0``.

    :param f_ck: Characteristic compressive strength of the concrete (MPa)
    :param t: Age of the structure (years)
    :param ur: Mean relative humidity, as a fraction in [0, 1]
    :param co_2: Atmospheric CO2 concentration (%)
    :param k_c: Factor related to the cement type (Table 3a)
    :param k_fc: Factor related to the compressive strength of the concrete (Table 3a)
    :param k_ad: Factor related to the pozzolanic additions of the concrete (Table 3a)
    :param k_co_2: Factor related to the CO2 concentration of the environment (Table 3a)
    :param k_rh: Factor related to the relative humidity (Table 3a)
    :param k_ce: Factor related to the exposure condition of the structure (Table 3b)
    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%)

    :return: Carbonation depth (mm)
    """

    f_ck = np.asarray(f_ck, dtype=float)
    t    = np.asarray(t, dtype=float)
    ur   = np.asarray(ur, dtype=float)
    co_2 = np.asarray(co_2, dtype=float)
    ad   = np.asarray(ad, dtype=float)

    if np.any(ur > 1.5):
        raise ValueError("`ur` must be a fraction in [0, 1] (0.70 for 70% RH), not a percentage.")

    aux_1  = k_c * (20.0 / f_ck) ** k_fc
    aux_2  = (t / 20.0) ** 0.5
    aux_31 = (k_ad * ad ** 1.5) / (40.0 + f_ck)
    aux_32 = (k_co_2 * co_2 ** 0.5) / (60.0 + f_ck)
    aux_33 = (k_rh * (ur - 0.58) ** 2) / (100.0 + f_ck)
    y_carb = aux_1 * aux_2 * np.exp(aux_31 + aux_32 - aux_33) * k_ce

    return y_carb


def carbonation_depth_possan_by_type(f_ck: np.ndarray | float, t: np.ndarray | float, ur: np.ndarray | float, co_2: np.ndarray | float, cement_type: int = 3, exposure_conditions: int = 2, ad: np.ndarray | float = 0.0) -> np.ndarray | float:
    """Convenience wrapper around `carbonation_depth_possan` that looks the six model coefficients up from the cement type and exposure condition, using the integer encodings adopted throughout this pipeline.

    :param f_ck: Characteristic compressive strength of the concrete (MPa)
    :param t: Age of the structure (years)
    :param ur: Mean relative humidity, as a fraction in [0, 1]
    :param co_2: Atmospheric CO2 concentration (%)
    :param cement_type: Type of cement (0: CP II Z, 1: CP V-ARI, 2: CP IV, 3: CP II F, 4: CP III, 5: CP II E, 6: CP I)
    :param exposure_conditions: Exposure conditions (0: PIA internal protected, 1: UEA external unprotected, 2: PEA external protected)
    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%)

    :return: Carbonation depth (mm)
    """

    coefficients = possan_coefficients(cement_type=cement_type, exposure_conditions=exposure_conditions)

    return carbonation_depth_possan(
                                       f_ck=f_ck, t=t, ur=ur, co_2=co_2, ad=ad,
                                       k_c=coefficients['k_c'], k_fc=coefficients['k_fc'], k_ad=coefficients['k_ad'],
                                       k_co_2=coefficients['k_co_2'], k_rh=coefficients['k_rh'], k_ce=coefficients['k_ce'],
                                   )


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


def emulator_function_time_durability(x: np.ndarray, names_x_variables: list, cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2, ad: float = 10.0, time_step: float = 0.0, n_latent_samples: int = 1000, n_starts: int = 15, seed: int = 42, verbose: bool = False, co2_scenario: str = "SSP2-4.5") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute the emulator of carbonation depth for durability analysis of reinforced concrete sections.

    The simulator is the closed-form Possan et al. (2016) carbonation model
    (`carbonation_depth_possan_by_type`) — no trained ML model is involved.

    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%), passed through
        to `carbonation_depth_possan_by_type`
    :param n_starts: Number of pyGLAM multi-start attempts per GLAM fit; each restart begins from a
        different point on the shape plane, which guards against the moment-matching optimizer
        settling in a poor local minimum (the failure mode that produced bad lambda 2 fits)
    :param seed: Seed used by pyGLAM to draw extra multi-start points once `n_starts` exceeds its
        fixed shape grid, for reproducible fits
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    co2_percentage_year(installation_year, co2_scenario)
    if not isinstance(time_step, Real) or not np.isfinite(time_step) or not 0 <= time_step <= 150:
        raise ValueError("time_step must be between 0 and 150 years.")
    co2_percentage_year(installation_year + time_step, co2_scenario)
    dfs = []
    start_year = installation_year
    year_query = start_year + time_step

    # =========================
    # 0. Time grid and CO2(%) profile
    # =========================
    lifetime_full  = 150
    grid_step      = 10
    grid_max       = min(lifetime_full, 2100 - start_year, grid_step * (int(np.ceil(max(time_step, 0) / grid_step)) + 1))
    years          = np.unique(np.append(np.arange(0, grid_max, grid_step), grid_max))
    calendar_years = start_year + years
    co2_values     = np.array([co2_percentage_year(y, co2_scenario) for y in calendar_years])
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

        t_grid   = np.tile(years, n_latent_samples)
        co2_grid = np.tile(co2_values, n_latent_samples)
        fck_grid = np.repeat(new_fck, n_grid)
        ur_grid  = np.repeat(new_rh, n_grid) / 100.0  # Possan model wants a fraction, not a percentage

        depths = carbonation_depth_possan_by_type(
                                                     f_ck=fck_grid, t=t_grid, ur=ur_grid, co_2=co2_grid,
                                                     cement_type=cement_type, exposure_conditions=exposure_conditions, ad=ad,
                                                   )
        depths = np.asarray(depths, dtype=float).reshape(n_latent_samples, n_grid)
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
                sol = emulator.fit_lambdas(df['g'].values, method="least_squares", n_starts=n_starts, seed=seed)
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

    for frame in (df_full, df_unique):
        frame.attrs["co2_scenario"] = co2_scenario
        frame.attrs["co2_source"] = "Meinshausen2017_2020"
    return df_full, df_unique


def generate_dataset_at_time_durability(x_train: np.ndarray, x_val: np.ndarray, time_step: float, cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2, ad: float = 10.0, n_latent_samples: int = 1000, n_starts: int = 15, seed: int = 42, output_dir: str | Path = '.', save: bool = True, verbose: bool = True, co2_scenario: str = "SSP2-4.5") -> dict:
    """Stage 1 of the split durability pipeline: run the emulator on the training and validation design samples at a single time step, and save both datasets to disk.

    This is the only stage that evaluates the Possan carbonation model, draws latent samples and fits the GLD — the expensive part that `Processing time (s)` measures. Splitting it from the PCE fit (`train_and_validate_pce_from_dataset_durability`) lets the dataset be generated once, in its own notebook, and the PCE refit or re-validated later without repeating any simulation.

    Artefacts are written to `output_dir` with the `<n_latent_samples>_<kind>_<split>_<time_step>_install_<year>_cement_<type>_exposure_<exposure>_co2_<scenario>.pkl` naming convention, where `<split>` is `train` or `val`.

    :param x_train: Design samples used to later train the PCE, shape (n_samples, 3) as [fck, rh, cover]
    :param x_val: Independent design samples used to later validate the PCE, shape (n_samples_validation, 3)
    :param time_step: Time step of the analysis [years]
    :param cement_type: Type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
    :param installation_year: Calendar year of installation
    :param exposure_conditions: Exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected])
    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%), passed through
        to `emulator_function_time_durability`
    :param n_latent_samples: Number of latent samples per design sample. Also used as the filename prefix
    :param n_starts: Number of pyGLAM multi-start attempts per GLAM fit, passed through to
        `emulator_function_time_durability`
    :param seed: Seed used by pyGLAM's multi-start, passed through to `emulator_function_time_durability`
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each split

    :return: Dictionary with the full/unique dataframes for the train and validation splits, the total emulator wall time, and the paths written
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    out_dir     = Path(output_dir)
    tag         = f'{time_step}_install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}_co2_{co2_scenario}'
    emulator_kw = dict(names_x_variables=["fck", "rh", "cov"], cement_type=cement_type,
                       installation_year=installation_year, exposure_conditions=exposure_conditions, co2_scenario=co2_scenario,
                       ad=ad, time_step=time_step, n_latent_samples=n_latent_samples, n_starts=n_starts, seed=seed, verbose=False)

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING DATASET FOR TIME STEP: {time_step} years')
        print(f'{"-"*40}')

    paths           = {}
    result          = {'time_step': time_step, 'co2_scenario': co2_scenario, 'paths': paths}
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


def train_and_validate_pce_from_dataset_durability(df_unique_train: pd.DataFrame, df_unique_val: pd.DataFrame, joint: Any, time_step: float, installation_year: int = 1990, cement_type: int = 3, exposure_conditions: int = 2, n_latent_samples: int = 1000, n_lambdas: int = 4, max_degree: int = 3, output_dir: str | Path = '.', save: bool = True, verbose: bool = True, co2_scenario: str = "SSP2-4.5") -> dict:
    """Stage 2 of the split durability pipeline: fit a PCE metamodel to a previously generated lambda dataset and validate it. Makes no emulator calls and draws no latent samples.

    Companion of `generate_dataset_at_time_durability`: takes its saved `dataset_unique` outputs (train and validation splits) and performs the PCE fit and scoring that `train_and_validate_pce_at_time` used to do inline with the data generation.

    Artefacts are written to `output_dir` with the same `<n_latent_samples>_<kind>_<time_step>_install_<year>_cement_<type>_exposure_<exposure>_co2_<scenario>.pkl` naming convention as `train_and_validate_pce_at_time`, so each scenario has separate dataset and metamodel files.

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
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    out_dir     = Path(output_dir)
    for frame in (df_unique_train, df_unique_val):
        if frame.attrs.get("co2_scenario") != co2_scenario or frame.attrs.get("co2_source") != "Meinshausen2017_2020":
            raise ValueError("Dataset CO2 metadata does not match. Regenerate the dataset with the selected SSP scenario.")
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'{time_step}_install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}_co2_{co2_scenario}'
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


def validate_pce_kl_divergence_durability(pce_metamodel: Any, fck: float, rh: float, cov: float, g_real: np.ndarray, lambda3: float, lambda4: float, n_grid: int = 400, random_state: int | np.random.Generator | None = 42) -> dict:
    r"""Score the PCE's predicted GLD against the raw Monte Carlo :math:`g` data, at one (fck, rh, cov) design point.

    Durability counterpart of `validate_pce_kl_divergence_benchmark` — same idea, three design
    variables instead of two. The PCE supplies lambda 1 / lambda 2 for `(fck, rh, cov)`; lambda 3 /
    lambda 4 are supplied by the caller, for the same reason as the benchmark: the PCE's own fit for
    those two is consistently poor.

    :param pce_metamodel: Fitted PCE for the time step `g_real` was computed at, as returned by `train_and_validate_pce_from_dataset_durability`
    :param fck: Compressive strength of the design point being checked (MPa)
    :param rh: Relative humidity of the design point being checked (%)
    :param cov: Cover of the design point being checked (mm)
    :param g_real: Raw Monte Carlo g samples for this design point (that design point's rows of `dataset_full`'s `g` column)
    :param lambda3: Fixed lambda 3 to pair with the PCE's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the PCE's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param random_state: Seed, NumPy Generator or None passed to pyGLAM's `rvs` for the fresh sample; see `_compare_gld_to_raw_benchmark`

    :return: Dictionary with the KL divergence, KS statistic, Wasserstein distance, R² between the two densities, relative errors at P5/P50/P95, the lambda vector used (plus the PCE's raw, unmodified prediction), the shared grid, both densities, and the fresh sample drawn from the PCE's GLD
    """

    lambda_pce_raw = np.asarray(pce_metamodel.predict(np.array([[fck, rh, cov]]))[0], dtype=float)
    lambda_pce     = np.array([lambda_pce_raw[0], lambda_pce_raw[1], lambda3, lambda4], dtype=float)

    result = _compare_gld_to_raw_benchmark(g_real, lambda_pce, n_grid=n_grid, random_state=random_state)
    result['lambda_pce']     = lambda_pce
    result['lambda_pce_raw'] = lambda_pce_raw
    result['pdf_pce']        = result.pop('pdf_pred')
    result['g_pce_samples']  = result.pop('g_pred_samples')

    return result


def validate_nn_kl_divergence_durability(models: dict, scaler: Any, fck: float, rh: float, cov: float, t: float, g_real: np.ndarray, lambda3: float, lambda4: float, n_grid: int = 400, random_state: int | np.random.Generator | None = 42) -> dict:
    r"""Score the global NN's predicted GLD against the raw Monte Carlo :math:`g` data, at one (fck, rh, cov, t) design point.

    Durability counterpart of `validate_nn_kl_divergence_benchmark`, for the global NN
    (`train_and_validate_nn_lambda_durability`) instead of the per-time-step PCE.

    :param models: ``{'lambda 1': fitted MLPRegressor, 'lambda 2': fitted MLPRegressor}``, as returned by `train_and_validate_nn_lambda_durability`
    :param scaler: The fitted `StandardScaler` for `(fck, rh, cov, t)`, as returned by `train_and_validate_nn_lambda_durability`
    :param fck: Compressive strength of the design point being checked (MPa)
    :param rh: Relative humidity of the design point being checked (%)
    :param cov: Cover of the design point being checked (mm)
    :param t: Time step of the design point being checked
    :param g_real: Raw Monte Carlo g samples for this design point (that design point's rows of `dataset_full`'s `g` column)
    :param lambda3: Fixed lambda 3 to pair with the NN's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the NN's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param random_state: Seed, NumPy Generator or None passed to pyGLAM's `rvs` for the fresh sample; see `_compare_gld_to_raw_benchmark`

    :return: Dictionary with the KL divergence, KS statistic, Wasserstein distance, R² between the two densities, relative errors at P5/P50/P95, the lambda vector used, the shared grid, both densities, and the fresh sample drawn from the NN's GLD
    """

    x_scaled  = scaler.transform(np.array([[fck, rh, cov, t]]))
    lambda_nn = np.array([float(models['lambda 1'].predict(x_scaled)[0]),
                          float(models['lambda 2'].predict(x_scaled)[0]),
                          lambda3,
                          lambda4], dtype=float)

    result = _compare_gld_to_raw_benchmark(g_real, lambda_nn, n_grid=n_grid, random_state=random_state)
    result['lambda_nn']    = lambda_nn
    result['pdf_nn']       = result.pop('pdf_pred')
    result['g_nn_samples'] = result.pop('g_pred_samples')

    return result


def validate_pce_kl_divergence_dataset_durability(pce_metamodel: Any, df_full: pd.DataFrame, time_step: float, lambda3: float, lambda4: float, n_grid: int = 400, max_points: int | None = None, random_state: int = 42, verbose: bool = True) -> pd.DataFrame:
    r"""Run `validate_pce_kl_divergence_durability` over every design point of one time step's `dataset_full`.

    Durability counterpart of `validate_pce_kl_divergence_dataset_benchmark` — groups `df_full` by
    design point `(fck, rh, cov)` instead of `(r, s)`, otherwise identical.

    :param pce_metamodel: Fitted PCE for `time_step`, as returned by `train_and_validate_pce_from_dataset_durability`
    :param df_full: That time step's `dataset_full` frame, one row per latent replica
    :param time_step: Time step being scored [years], copied into the output frame
    :param lambda3: Fixed lambda 3 to pair with the PCE's lambda 1 / lambda 2
    :param lambda4: Fixed lambda 4 to pair with the PCE's lambda 1 / lambda 2
    :param n_grid: Number of grid points used to numerically integrate the KL divergence and R²
    :param max_points: Score only `max_points` design points, drawn at random from the ones present. None scores all of them
    :param random_state: Seed for the whole sweep; see `validate_pce_kl_divergence_dataset_benchmark`
    :param verbose: Whether to print progress

    :return: One row per design point, with `fck`, `rh`, `cov`, `Time (years)` and the seven statistics
    """

    rng     = np.random.default_rng(random_state)
    grouped = list(df_full.groupby(['fck', 'rh', 'cov'], sort=False))

    if max_points is not None and max_points < len(grouped):
        grouped = [grouped[i] for i in np.sort(rng.choice(len(grouped), size=max_points, replace=False))]

    if verbose:
        print(f'  t = {time_step:.2f} years: scoring {len(grouped)} design points')

    rows = []
    for (fck, rh, cov), group in grouped:
        stats_ = validate_pce_kl_divergence_durability(
                                                          pce_metamodel=pce_metamodel,
                                                          fck=fck,
                                                          rh=rh,
                                                          cov=cov,
                                                          g_real=group['g'].to_numpy(),
                                                          lambda3=lambda3,
                                                          lambda4=lambda4,
                                                          n_grid=n_grid,
                                                          random_state=rng,
                                                      )
        rows.append({
                        'fck':           fck,
                        'rh':            rh,
                        'cov':           cov,
                        'Time (years)':  time_step,
                        'KL':            stats_['kl_divergence'],
                        'KS':            stats_['ks_statistic'],
                        'Wasserstein':   stats_['wasserstein'],
                        'R2 (PDF)':      stats_['r2_pdf'],
                        'Rel. error P5':  stats_['rel_err_p5'],
                        'Rel. error P50': stats_['rel_err_p50'],
                        'Rel. error P95': stats_['rel_err_p95'],
                    })

    df_out    = pd.DataFrame(rows)
    n_invalid = int(df_out['KL'].isna().sum())
    if verbose and n_invalid:
        print(f'    {n_invalid} design point(s) scored NaN — the PCE predicted an invalid GLD (lambda 2 <= 0) there')

    return df_out


def generate_nn_dataset_durability(pce_metamodels: list, times: np.ndarray, joint: Any, installation_year: int = 1990, cement_type: int = 3, exposure_conditions: int = 2, co2_scenario: str = "SSP2-4.5", n_points: int = 5000, n_lambdas: int = 4, lambda3_fixed: float | None = None, lambda4_fixed: float | None = None, n_latent_samples: int = 1000, output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Build the (fck, rh, cov, t) -> lambda dataset used to train a single global NN surrogate, by querying the per-time-step PCE metamodels instead of re-running the stochastic emulator.

    Durability counterpart of `generate_nn_dataset_benchmark` — three design variables instead of
    two, and the filename carries the same install/cement/exposure/co2 tag as the rest of the
    durability pipeline instead of the bare `_benchmark` suffix.

    Artefacts are written to `output_dir` as `<n_latent_samples>_dataset_nn_durability_install_<year>_cement_<type>_exposure_<exposure>_co2_<scenario>.pkl`.

    :param pce_metamodels: Fitted `PolynomialChaosExpansion` models, one per entry of `times`, in the same order (as saved by `train_and_validate_pce_from_dataset_durability`)
    :param times: Time steps to stack into the dataset [years], paired positionally with `pce_metamodels`
    :param joint: UQpy JointIndependent distribution of fck, rh and cov, used to draw the query points fed to each PCE
    :param installation_year: Calendar year of installation. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param cement_type: Type of cement. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param exposure_conditions: Exposure conditions. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5. Only used for the filename, to match `generate_dataset_at_time_durability`
    :param n_points: Number of (fck, rh, cov) query points drawn per time step
    :param n_lambdas: Number of GLD lambdas predicted by the PCE
    :param lambda3_fixed: If given, overrides the PCE's predicted `lambda 3` column with this fixed value for every row. If None, keeps the PCE prediction
    :param lambda4_fixed: If given, overrides the PCE's predicted `lambda 4` column with this fixed value for every row. If None, keeps the PCE prediction
    :param n_latent_samples: Number of latent samples used to fit `pce_metamodels`. Only used for the filename prefix, to match `train_and_validate_pce_from_dataset_durability`
    :param output_dir: Directory where the .pkl artefact is written
    :param save: Whether to write the .pkl artefact to disk
    :param verbose: Whether to print the progress of each time step

    :return: Dictionary with the stacked dataframe and the path written
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    out_dir     = Path(output_dir)
    lambda_cols = [f'lambda {i}' for i in range(1, n_lambdas + 1)]
    tag         = f'install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}_co2_{co2_scenario}'

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING NN DATASET FROM {len(times)} PCE MODELS')
        print(f'{"-"*40}')
        if lambda3_fixed is not None:
            print(f'  lambda 3 fixed at {lambda3_fixed:.4f}')
        if lambda4_fixed is not None:
            print(f'  lambda 4 fixed at {lambda4_fixed:.4f}')

    # =========================
    # 1. Query each time step's PCE at fresh (fck, rh, cov) points
    # =========================
    dfs = []
    for t, pce_metamodel in zip(times, pce_metamodels):
        x      = joint.rvs(n_points)
        y_pred = pce_metamodel.predict(x)

        df = pd.DataFrame(x, columns=['fck', 'rh', 'cov'])
        df.insert(3, 'Time (years)', t)
        df[lambda_cols] = y_pred
        if lambda3_fixed is not None and 'lambda 3' in lambda_cols:
            df['lambda 3'] = lambda3_fixed
        if lambda4_fixed is not None and 'lambda 4' in lambda_cols:
            df['lambda 4'] = lambda4_fixed
        dfs.append(df)

        if verbose:
            print(f'  t = {t:.2f} years: {n_points} points queried from the PCE')

    df_nn = pd.concat(dfs, ignore_index=True)

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths['dataset_nn'] = out_dir / f'{n_latent_samples}_dataset_nn_durability_{tag}.pkl'
        with open(paths['dataset_nn'], 'wb') as f:
            dill.dump(df_nn, f)
        if verbose:
            print('The NN dataset has been saved!')

    return {
             'dataset_nn': df_nn,
             'paths':      paths,
           }


def train_and_validate_nn_lambda_durability(df_nn: pd.DataFrame, feature_cols: list = ['fck', 'rh', 'cov', 'Time (years)'], target_cols: list = ['lambda 1', 'lambda 2'], test_frac: float = 0.2, hidden_layer_sizes: tuple = (64, 64), max_iter: int = 500, n_iter_no_change: int = 15, random_state: int = 42, n_latent_samples: int = 1000, installation_year: int = 1990, cement_type: int = 3, exposure_conditions: int = 2, co2_scenario: str = "SSP2-4.5", output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Fit one MLPRegressor per target lambda on (fck, rh, cov, t) -> lambda, the global NN counterpart of the per-time-step PCE.

    Durability counterpart of `train_and_validate_nn_lambda_benchmark` — same workflow, three design
    variables instead of two, and the durability install/cement/exposure/co2 tag in every filename.
    Only `target_cols` (by default lambda 1 and lambda 2) are modelled here — the remaining lambdas
    are meant to be read back from the emulator dataset directly, not predicted by this function.

    Rows with a NaN in any `target_cols` (design points where the GLD fit failed) are dropped before the split.

    Artefacts are written to `output_dir` as `<n_latent_samples>_nn_<target>_model_durability_<tag>.pkl` (one per target), `<n_latent_samples>_nn_scaler_durability_<tag>.pkl`, and `<n_latent_samples>_nn_validation_stats_durability_<tag>.pkl`, where `<tag>` is `install_<year>_cement_<type>_exposure_<exposure>_co2_<scenario>`.

    :param df_nn: Stacked dataset from `generate_nn_dataset_durability`, one row per (design point, time step)
    :param feature_cols: Input columns for the NN, in order
    :param target_cols: Lambda columns to fit one model each for
    :param test_frac: Fraction of the (NaN-dropped) rows held out for validation
    :param hidden_layer_sizes: Hidden layer sizes, shared by every target's MLPRegressor
    :param max_iter: Maximum training iterations per MLPRegressor
    :param n_iter_no_change: Early-stopping patience
    :param random_state: Seed for the split and every MLPRegressor's initialisation
    :param n_latent_samples: Number of latent samples used to build `df_nn`. Only used for the filename prefix, to match `generate_nn_dataset_durability`
    :param installation_year: Calendar year of installation. Only used for the filename, to match `generate_nn_dataset_durability`
    :param cement_type: Type of cement. Only used for the filename, to match `generate_nn_dataset_durability`
    :param exposure_conditions: Exposure conditions. Only used for the filename, to match `generate_nn_dataset_durability`
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5. Only used for the filename, to match `generate_nn_dataset_durability`
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the fitted models (one per target), the fitted scaler, the validation statistics, and the paths written
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    out_dir   = Path(output_dir)
    tag       = f'install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}_co2_{co2_scenario}'
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
            paths[key] = out_dir / f'{n_latent_samples}_nn_{key}_model_durability_{tag}.pkl'
            with open(paths[key], 'wb') as f:
                dill.dump(model, f)

        paths['scaler'] = out_dir / f'{n_latent_samples}_nn_scaler_durability_{tag}.pkl'
        with open(paths['scaler'], 'wb') as f:
            dill.dump(scaler, f)

        paths['nn_validation_stats'] = out_dir / f'{n_latent_samples}_nn_validation_stats_durability_{tag}.pkl'
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


def generate_rul_dataset_durability(fck: float, rh: float, cov: float, times: np.ndarray, n_latent_samples: int = 1000, installation_year: int = 1990, cement_type: int = 3, exposure_conditions: int = 2, co2_scenario: str = "SSP2-4.5", lambda3_fixed: float | None = None, lambda4_fixed: float | None = None, n_glam_samples: int = 10000, random_state: int = 42, input_dir: str | Path = '.', output_dir: str | Path = '.', save: bool = True, verbose: bool = True) -> dict:
    """Predict lambda 1/2 at a fixed (fck, rh, cov) across a grid of time steps with the trained global NN, fix lambda 3/4, and draw GLD Monte Carlo samples of g at each time step.

    Durability counterpart of `generate_rul_dataset_benchmark` — three design variables instead of
    two, otherwise identical: the raw material for a spaghetti / RUL plot on `g = cover -
    carbonation depth`.

    Loads the artefacts written by `train_and_validate_nn_lambda_durability` from `input_dir`. If
    `lambda3_fixed`/`lambda4_fixed` are not given, they default to the mean of `lambda 3`/`lambda 4`
    over `generate_nn_dataset_durability`'s own training dataset, also read from `input_dir`.

    Artefacts are written to `output_dir` as ``<n_latent_samples>_rul_lambdas_fck<fck>_rh<rh>_cov<cov>_durability.pkl``
    (the per-time-step lambda dataframe) and ``<n_latent_samples>_rul_samples_fck<fck>_rh<rh>_cov<cov>_durability.pkl``
    (the raw Monte Carlo samples).

    :param fck: Fixed compressive strength to query (MPa)
    :param rh: Fixed relative humidity to query (%)
    :param cov: Fixed cover to query (mm)
    :param times: Time steps to sweep [years]
    :param n_latent_samples: Number of latent samples used to train the NN. Only used for the filename prefix, to match `train_and_validate_nn_lambda_durability`
    :param installation_year: Calendar year of installation. Only used for the filename, to match `train_and_validate_nn_lambda_durability`
    :param cement_type: Type of cement. Only used for the filename, to match `train_and_validate_nn_lambda_durability`
    :param exposure_conditions: Exposure conditions. Only used for the filename, to match `train_and_validate_nn_lambda_durability`
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5. Only used for the filename, to match `train_and_validate_nn_lambda_durability`
    :param lambda3_fixed: Fixed value for lambda 3. If None, uses the mean over the NN training dataset
    :param lambda4_fixed: Fixed value for lambda 4. If None, uses the mean over the NN training dataset
    :param n_glam_samples: Number of Monte Carlo samples drawn from the GLD at each time step
    :param random_state: Seed passed unchanged to `GlamFKML.rvs` at every time step; see `generate_rul_dataset_benchmark`
    :param input_dir: Directory the NN artefacts (and, if needed, the NN training dataset) are read from
    :param output_dir: Directory where the .pkl artefacts are written
    :param save: Whether to write the .pkl artefacts to disk
    :param verbose: Whether to print the progress of each stage

    :return: Dictionary with the per-time-step lambda dataframe, the Monte Carlo samples (shape ``(n_glam_samples, len(times))``), the fixed lambda 3/4 used, and the paths written
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    in_dir  = Path(input_dir)
    out_dir = Path(output_dir)
    times   = np.asarray(times, dtype=float)
    tag     = f'install_{installation_year}_cement_{cement_type}_exposure_{exposure_conditions}_co2_{co2_scenario}'

    if verbose:
        print(f'\n{"-"*40}')
        print(f'GENERATING RUL DATASET AT fck={fck}, rh={rh}, cov={cov}')
        print(f'{"-"*40}')

    # =========================
    # 1. Load the trained NN (lambda 1, lambda 2) and its scaler
    # =========================
    with open(in_dir / f'{n_latent_samples}_nn_lambda_1_model_durability_{tag}.pkl', 'rb') as f:
        model_l1 = dill.load(f)
    with open(in_dir / f'{n_latent_samples}_nn_lambda_2_model_durability_{tag}.pkl', 'rb') as f:
        model_l2 = dill.load(f)
    with open(in_dir / f'{n_latent_samples}_nn_scaler_durability_{tag}.pkl', 'rb') as f:
        scaler = dill.load(f)

    # =========================
    # 2. Default lambda 3 / lambda 4, if not given
    # =========================
    if lambda3_fixed is None or lambda4_fixed is None:
        with open(in_dir / f'{n_latent_samples}_dataset_nn_durability_{tag}.pkl', 'rb') as f:
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
    lambda_df    = pd.DataFrame({'fck': fck, 'rh': rh, 'cov': cov, 'Time (years)': times})
    query_scaled = scaler.transform(lambda_df[['fck', 'rh', 'cov', 'Time (years)']].to_numpy())
    lambda_df['lambda 1'] = model_l1.predict(query_scaled)
    lambda_df['lambda 2'] = model_l2.predict(query_scaled)
    lambda_df['lambda 3'] = lambda3_fixed
    lambda_df['lambda 4'] = lambda4_fixed

    # =========================
    # 4. GLD Monte Carlo samples of g at each time step
    # =========================
    # Same comonotonic-path construction as `generate_rul_dataset_benchmark` — see its docstring for
    # why the quantile level is held fixed across time instead of drawing each column independently.
    samples = np.empty((n_glam_samples, len(times)))
    for i, row in lambda_df.iterrows():
        model         = glam.GlamFKML(row['lambda 1'], row['lambda 2'], row['lambda 3'], row['lambda 4'])
        samples[:, i] = model.rvs(size=n_glam_samples, quantile_trim=0.0, random_state=random_state)
        if verbose:
            print(f'  t = {row["Time (years)"]:.1f}: lambda 1 = {row["lambda 1"]:.3f}, lambda 2 = {row["lambda 2"]:.3f}, '
                  f'sample mean = {samples[:, i].mean():.3f}, sample std = {samples[:, i].std():.3f}')

    paths = {}
    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        rul_tag = f'fck{fck:g}_rh{rh:g}_cov{cov:g}_durability'
        paths['lambda_df'] = out_dir / f'{n_latent_samples}_rul_lambdas_{rul_tag}.pkl'
        with open(paths['lambda_df'], 'wb') as f:
            dill.dump(lambda_df, f)
        paths['samples'] = out_dir / f'{n_latent_samples}_rul_samples_{rul_tag}.pkl'
        with open(paths['samples'], 'wb') as f:
            dill.dump(samples, f)
        if verbose:
            print('The RUL lambda dataframe and Monte Carlo samples have been saved!')

    return {
             'lambda_df':     lambda_df,
             'samples':       samples,
             'times':         times,
             'fck':           fck,
             'rh':            rh,
             'cov':           cov,
             'lambda3_fixed': lambda3_fixed,
             'lambda4_fixed': lambda4_fixed,
             'paths':         paths,
           }


# =============================================================================
# PYGLAM VERIFICATION — GLD fitted to reference distributions, used by 00_pyglam_test
# =============================================================================


def gld_quantile_at_u(lambdas: np.ndarray | list, u: np.ndarray | float) -> np.ndarray:
    r"""Quantile function of the FKML-parameterized GLD, evaluated in closed form.

    .. math::

        Q(u) = \lambda_1 + \frac{1}{\lambda_2}\left(\frac{u^{\lambda_3}-1}{\lambda_3}
               - \frac{(1-u)^{\lambda_4}-1}{\lambda_4}\right)

    Equivalent to `pyglam.GlamFKML.ppf`, but without its numerical root-finding, which makes
    it usable on large grids and as an exact inverse-transform sampler.

    :param lambdas: The four GLD parameters, ordered as lambda_1 to lambda_4
    :param u: Cumulative probability (or array of probabilities) in (0, 1)

    :return: Quantile of the GLD at u
    """

    l1, l2, l3, l4 = lambdas

    return l1 + ((u ** l3 - 1.0) / l3 - ((1.0 - u) ** l4 - 1.0) / l4) / l2


def gld_density_at_u(lambdas: np.ndarray | list, u: np.ndarray | float) -> np.ndarray:
    r"""Density of the FKML-parameterized GLD at the point x = Q(u), in closed form.

    Since the GLD is defined by its quantile function, its density satisfies
    :math:`q(Q(u)) = 1/Q'(u)` with
    :math:`Q'(u) = \left[u^{\lambda_3-1} + (1-u)^{\lambda_4-1}\right]/\lambda_2`. Evaluating it
    this way avoids the CDF inversion that `pyglam.GlamFKML.pdf` performs internally — a
    round trip whose numerical error is large enough to turn a well-fitted Kullback--Leibler
    integral slightly negative.

    :param lambdas: The four GLD parameters, ordered as lambda_1 to lambda_4
    :param u: Cumulative probability (or array of probabilities) in (0, 1)

    :return: Density of the GLD at x = Q(u)
    """

    _, l2, l3, l4 = lambdas

    return l2 / (u ** (l3 - 1.0) + (1.0 - u) ** (l4 - 1.0))


def gld_support(lambdas: np.ndarray | list, eps: float = 1e-12) -> tuple[float, float]:
    """Endpoints of the support of a fitted GLD, finite whenever lambda_3 > 0 and lambda_4 > 0.

    :param lambdas: The four GLD parameters, ordered as lambda_1 to lambda_4
    :param eps: Offset from 0 and 1 used to evaluate the endpoints

    :return: Lower and upper endpoints of the support
    """

    return float(gld_quantile_at_u(lambdas, eps)), float(gld_quantile_at_u(lambdas, 1.0 - eps))


def fit_gld_to_sample(sample: np.ndarray, n_starts: int = 15, seed: int = 42) -> np.ndarray:
    """Fit the four GLD parameters to a sample by the method of moments, via pyGLAM.

    :param sample: Sample the GLD is fitted to
    :param n_starts: Number of pyGLAM multi-start attempts
    :param seed: Seed used by pyGLAM's multi-start

    :return: The four fitted GLD parameters, ordered as lambda_1 to lambda_4
    """

    sol = glam.GlamFKML().fit_lambdas(np.asarray(sample, dtype=float), method='least_squares',
                                      n_starts=n_starts, seed=seed)

    return np.asarray(sol.x, dtype=float)


def kl_divergence_gld(dist: Any, lambdas: np.ndarray | list, n_grid: int = 20001, eps: float = 1e-9) -> float:
    r"""Kullback--Leibler divergence :math:`D(q\|p)` of a fitted GLD q from an analytical target p.

    This is the only finite direction here: in the FKML parameterization with
    :math:`\lambda_3, \lambda_4 > 0` the GLD has compact support, whereas the Normal, Gumbel and
    Lognormal targets do not — so :math:`D(p\|q)` diverges by construction. The integral is taken
    in cumulative-probability space (:math:`x = Q(u)`, :math:`\mathrm{d}u = q(x)\,\mathrm{d}x`),
    which sidesteps having to locate the endpoints of the support:

    .. math::

        D(q\|p) = \mathbb{E}_q\!\left[\log \frac{q}{p}\right]
                = \int_0^1 \log \frac{q(Q(u))}{p(Q(u))}\,\mathrm{d}u

    :param dist: Frozen `scipy.stats` distribution playing the role of the target p
    :param lambdas: The four fitted GLD parameters
    :param n_grid: Number of quadrature points in u
    :param eps: Offset from 0 and 1, keeping the integrable endpoint singularities finite

    :return: Kullback--Leibler divergence, in nats
    """

    u = np.linspace(eps, 1.0 - eps, n_grid)
    q = gld_density_at_u(lambdas, u)
    p = dist.pdf(gld_quantile_at_u(lambdas, u))
    m = np.isfinite(q) & np.isfinite(p) & (q > 1e-300) & (p > 1e-300)

    return float(simpson(np.log(q[m] / p[m]), x=u[m]))


def ks_distance_to_target(dist: Any, lambdas: np.ndarray | list, n_grid: int = 20001, eps: float = 1e-9) -> float:
    """Kolmogorov--Smirnov distance between the fitted GLD CDF and the analytical target CDF.

    Unlike a two-sample test, this is a deterministic measure of how well the GLD *family*
    approximates the target, free of sampling noise. Walking the support through the GLD's own
    quantile function makes the statistic ``sup_u |u - F_target(Q(u))|``, since the GLD CDF at
    ``x = Q(u)`` is exactly ``u``.

    :param dist: Frozen `scipy.stats` distribution playing the role of the target
    :param lambdas: The four fitted GLD parameters
    :param n_grid: Number of points spanning the support
    :param eps: Offset from 0 and 1

    :return: Supremum of the absolute difference between the two CDFs
    """

    u = np.linspace(eps, 1.0 - eps, n_grid)

    return float(np.nanmax(np.abs(u - dist.cdf(gld_quantile_at_u(lambdas, u)))))


def evaluate_gld_fit(name: str, dist: Any, n: int, seed: int = 42, n_starts: int = 15, n_ref: int = 20000) -> dict:
    """Draw one sample from a target distribution, fit a GLD to it and score the fit.

    :param name: Label of the target distribution, carried through to the results table
    :param dist: Frozen `scipy.stats` distribution to sample from and compare against
    :param n: Sample size
    :param seed: Seed of the sample and of pyGLAM's multi-start
    :param n_starts: Number of pyGLAM multi-start attempts
    :param n_ref: Size of the GLD sample used for the two-sample tests

    :return: Dictionary with the fitted lambdas, goodness-of-fit metrics and support endpoints
    """

    rng     = np.random.default_rng(seed)
    sample  = dist.rvs(size=n, random_state=rng)
    lambdas = fit_gld_to_sample(sample, n_starts=n_starts, seed=seed)

    quantiles = np.array([0.05, 0.50, 0.95])
    q_target  = dist.ppf(quantiles)
    q_gld     = gld_quantile_at_u(lambdas, quantiles)
    spread    = dist.ppf(0.95) - dist.ppf(0.05)
    err_q     = np.abs(q_gld - q_target) / spread * 100.0

    # inverse-transform sampling in closed form: exact, and far cheaper than GlamFKML.rvs
    gld_sample = gld_quantile_at_u(lambdas, rng.uniform(1e-9, 1.0 - 1e-9, size=max(n, n_ref)))
    ks_two     = ks_2samp(sample, gld_sample)
    support    = gld_support(lambdas)

    return {'Distribution': name, 'N': n,
            'lambda 1': lambdas[0], 'lambda 2': lambdas[1], 'lambda 3': lambdas[2], 'lambda 4': lambdas[3],
            'KS': ks_distance_to_target(dist, lambdas),
            'KS 2-sample': ks_two.statistic, 'p-value': ks_two.pvalue,
            'KL': kl_divergence_gld(dist, lambdas),
            'Wasserstein': float(wasserstein_distance(sample, gld_sample)),
            'err P5 (%)': err_q[0], 'err P50 (%)': err_q[1], 'err P95 (%)': err_q[2],
            'support min': support[0], 'support max': support[1]}


def study_gld_fits(targets: dict, sizes: tuple, n_rep: int = 20, n_starts: int = 15, base_seed: int = 0, verbose: bool = True) -> pd.DataFrame:
    """Repeat `evaluate_gld_fit` over independent samples for every (distribution, sample size) cell.

    Replication matters here: a single fit at N = 50 is dominated by sampling noise, so the
    convergence of the method of moments only becomes legible in the average over replicates.

    :param targets: Mapping from label to frozen `scipy.stats` distribution
    :param sizes: Sample sizes to sweep
    :param n_rep: Number of independent replicates per cell
    :param n_starts: Number of pyGLAM multi-start attempts per fit
    :param base_seed: Base seed; each replicate offsets it
    :param verbose: Whether to report progress per distribution

    :return: DataFrame with one row per replicate
    """

    rows = []
    for name, dist in targets.items():
        if verbose:
            print(f'  {name} ...', end='', flush=True)
        for n in sizes:
            for r in range(n_rep):
                row = evaluate_gld_fit(name, dist, n, seed=base_seed + 1000 * r + n, n_starts=n_starts)
                row['rep'] = r
                rows.append(row)
        if verbose:
            print(' done')

    return pd.DataFrame(rows)


# =============================================================================
# LEGACY / UNUSED — not called by any current *_final notebook, kept for reference
# =============================================================================

def carbonation_profile(model_: Any, lifetime: float, fc: float, rh: float, cement_type: int, exposure: int, start_year: int, co2_scenario: str = "SSP2-4.5") -> pd.DataFrame:
    """Generate carbonation profile starting at a given calendar year.

    :param model_: trained ML model for carbonation depth prediction, which should have a method .predict() and an attribute .feature_names_in_ that contains the names of the features used for training.
    :param lifetime: Design life of the structure [years]
    :param fc: Concrete compressive strength [MPa]
    :param rh: Relative humidity [%]
    :param cement_type: Type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
    :param exposure: Exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected])
    :param start_year: Calendar year of installation

    :return: DataFrame with columns C02 concentration (%), compressive strength (MPa), relative humidity (%), type of cement, exposure conditions, year, and carbonation depth (mm)
    :param co2_scenario: SSP1-2.6, SSP2-4.5 (default), or SSP5-8.5
    """

    co2_scenario = _co2_scenario_name(co2_scenario)
    co2_percentage_year(start_year, co2_scenario)
    if not isinstance(lifetime, Real) or not np.isfinite(lifetime) or lifetime < 0:
        raise ValueError("lifetime must be a finite nonnegative number of years.")
    co2_percentage_year(start_year + lifetime, co2_scenario)
    # Include the requested endpoint without querying CO2 beyond 2100.
    years = np.unique(np.append(np.arange(0, lifetime, 10), lifetime))

    # Romain calendar
    calendar_years = start_year + years

    # Atmospheric CO2 concentration
    co2_values = [co2_percentage_year(y, co2_scenario) for y in calendar_years]

    # Carbonation AI model and profile
    df      = pd.DataFrame({'t (years)': years, 'CO2 (%)': co2_values, 'fc (MPa)': [fc]*len(years), 'RH (%)': [rh]*len(years), 'Type of cement': [cement_type]*len(years), 'Exposure conditions': [exposure]*len(years)})
    df      = df[model_.feature_names_in_]
    depth   = model_.predict(df)
    profile = pd.DataFrame({'calendar year': calendar_years, 't (years)': years, 'CO2 (%)': co2_values, 'carbonation depth (mm)': depth})
    profile['carbonation depth (mm)'] = profile['carbonation depth (mm)'].cummax()

    profile.attrs["co2_scenario"] = co2_scenario
    return profile

