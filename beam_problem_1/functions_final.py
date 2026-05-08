import os
from pathlib import Path
from pyexpat import model

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
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import scipy.stats as stats
from multiprocessing import Pool, cpu_count
from scipy.interpolate import interp1d
import scipy as sc
import joblib
import pyglam as glam


def execute_parallel_process(k: float | int, n_samples: int, n_latent_samples: int) -> dict:
    """Execute parallel process for training, saving, and validating the PCE metamodel at time k.
    
    :param k: Time parameter affecting the state limit function
    :param n_samples: Number of samples for training and validation
    :param n_latent_samples: Number of latent samples to be generated for each input sample
    
    :return: Formatted string with R2 score for time k
    """
    
    # 1. Training
    r = Normal(loc=5., scale=0.8)
    s = Normal(loc=2., scale=0.6)
    joint = JointIndependent(marginals=[r, s])
    x = joint.rvs(n_samples)
    y, _ = state_limit_function_time(x, n_latent_samples, t=k)
    max_degree = 3
    polynomial_basis = TotalDegreeBasis(joint, max_degree)
    least_squares = LeastSquareRegression()
    pce_metamodel = PolynomialChaosExpansion(polynomial_basis=polynomial_basis, regression_method=least_squares)
    pce_metamodel.fit(x, y)
    
    # 2. Save metamodel
    filename = f'pce_metamodel_{k}.pkl'
    with open(filename, 'wb') as f:
        dill.dump(pce_metamodel, f)
    
    # 3. Validation
    r_val = Normal(loc=5., scale=0.8)
    s_val = Normal(loc=2., scale=0.6)
    joint_val = JointIndependent(marginals=[r_val, s_val])
    x_val = joint_val.rvs(n_samples)
    y_val_obs, _ = state_limit_function_time(x_val, n_latent_samples, t=k)
    with open(filename, 'rb') as f:
        pce_metamodel_up = pickle.load(f)
    y_val_pre = pce_metamodel_up.predict(x_val)
    y_val_obs_aux_lambda_1 = list(y_val_obs[:, 0])
    y_val_pre_aux_lambda_1 = list(y_val_pre[:, 0])
    y_val_obs_aux_lambda_2 = list(y_val_obs[:, 1])
    y_val_pre_aux_lambda_2 = list(y_val_pre[:, 1])
    y_val_obs_aux_lambda_3 = list(y_val_obs[:, 2])
    y_val_pre_aux_lambda_3 = list(y_val_pre[:, 2])
    y_val_obs_aux_lambda_4 = list(y_val_obs[:, 3])
    y_val_pre_aux_lambda_4 = list(y_val_pre[:, 3])
           
    # R2 scores
    score_lambda_1 = r2_score(y_val_obs_aux_lambda_1, y_val_pre_aux_lambda_1)
    score_lambda_2 = r2_score(y_val_obs_aux_lambda_2, y_val_pre_aux_lambda_2)
    score_lambda_3 = r2_score(y_val_obs_aux_lambda_3, y_val_pre_aux_lambda_3)
    score_lambda_4 = r2_score(y_val_obs_aux_lambda_4, y_val_pre_aux_lambda_4) 
    
    return {
            'Time': k,
            'R2 (Lambda 1)': score_lambda_1,
            'R2 (Lambda 2)': score_lambda_2,
            'R2 (Lambda 3)': score_lambda_3,
            'R2 (Lambda 4)': score_lambda_4
           }


def pce_toy_problem_parallel_with_multiprocessing(n_samples: int = 1000, n_latent_samples: int = 5000) -> list:
    """Execute PCE training process and validate.
    
    :return: r2 score about PCE training
    """

    time = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    inputs = [(k, n_samples, n_latent_samples) for k in time]

    # Execution
    n_processes = cpu_count()
    with Pool(processes=n_processes) as pool:
        results = pool.starmap(execute_parallel_process, inputs)

    return results


def g_toy_problem_parallel_with_multiprocessing(x_val_list: np.ndarray | list, n_latent_samples: int, t: float = 0.0, n_processes: Optional[int] = None):
    """Execute the state limit function in parallel using multiprocessing.

    :param x_val_list: R and S realization dividided in batches for parallel processing
    :param n_latent_samples: Number of latent samples to be generated for each input sample
    :param t: Time step. Default is 0
    :param n_processes: Number of processes to use. If None, use the number of CPU cores

    :return: [0] All datat and [1] Dataset with GLAM parameters and state limit function results for each batch
    """

    if n_processes is None:
        n_processes = cpu_count()
    args_list = [(x_val_list[i], n_latent_samples, t) for i in range(len(x_val_list))]
    with Pool(processes=n_processes) as pool:
        results = pool.starmap(state_limit_function_time, args_list)
    y_list = [r[0] for r in results]
    df_list = [r[1] for r in results]
    df = []
    i = 0
    for j, sublist in enumerate(df_list):
        for k, item in enumerate(sublist):
            item['realization'] = i
            item["lambda 1"] = y_list[j][k][0]
            item["lambda 2"] = y_list[j][k][1]
            item["lambda 3"] = y_list[j][k][2]
            item["lambda 4"] = y_list[j][k][3]
            i += 1
            df.append(item)
    df = pd.concat(df).reset_index(drop=True)
    df['time'] = t
    df = df[['realization', 'time', 'r', 's', 'z1', 'z2', 'g', 'lambda 1', 'lambda 2', 'lambda 3', 'lambda 4']]
    glam_data = {'r': [], 's': [], 'lambda 1': [], 'lambda 2': [], 'lambda 3': [], 'lambda 4': []}
    n_samples = df['realization'].nunique()
    for i in range(n_samples):
        x = df[df['realization'] == i]
        r, s, lambda_1, lambda_2, lambda_3, lambda_4 = x['r'].values[0], x['s'].values[0], x['lambda 1'].values[0], x['lambda 2'].values[0], x['lambda 3'].values[0], x['lambda 4'].values[0]
        glam_data['r'].append(r)
        glam_data['s'].append(s)
        glam_data['lambda 1'].append(lambda_1)
        glam_data['lambda 2'].append(lambda_2)
        glam_data['lambda 3'].append(lambda_3)
        glam_data['lambda 4'].append(lambda_4)
    glam_data = pd.DataFrame(glam_data)

    return df, glam_data


def g_interpolated_at_t(bds, t_query, column='g_emulator_mean'):
    """
    Retorna g(t_query) por interpolação linear.
    """
    t = bds['time'].values
    g = bds[column].values

    f = interp1d(
        t, g,
        kind='linear',
        fill_value='extrapolate',
        bounds_error=False
    )

    return float(f(t_query))


def failure_time_interpolated(bds, g_threshold=0.0, column='g_emulator_mean'):
    """
    Retorna o tempo exato de falha por interpolação (g = g_threshold).
    """
    t = bds['time'].values
    g = bds[column].values

    # Detecta cruzamento
    sign_change = np.where(np.diff(np.sign(g - g_threshold)) != 0)[0]

    if len(sign_change) == 0:
        return None  # nunca falha no horizonte analisado

    i = sign_change[0]

    # Interpolação linear entre os dois pontos
    t1, t2 = t[i], t[i + 1]
    g1, g2 = g[i], g[i + 1]

    t_failure = t1 + (g_threshold - g1) * (t2 - t1) / (g2 - g1)

    return float(t_failure)


def rul(df, t_i, g_threshold, g_column='g_emulator_mean'):
    """
    Compute Remaining Useful Life (RUL) based on g(t)

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns ['time', g_column]
    t_i : float
        Inspection time
    g_threshold : float
        Failure threshold (usually 0)
    g_column : str
        Column name of g(t)

    Returns
    -------
    dict
    """

    # Ordenar por tempo
    df = df.sort_values('time')

    time = df['time'].values
    g = df[g_column].values

    # -------------------------
    # Interpolação em t_i
    # -------------------------
    g_ti = np.interp(t_i, time, g)

    # Já falhou?
    if g_ti <= g_threshold:
        return {
            't_inspection': t_i,
            't_failure': t_i,
            'RUL': 0.0,
            'g_at_inspection': g_ti
        }

    # -------------------------
    # Tempo de falha (g = threshold)
    # -------------------------
    idx = np.where(g <= g_threshold)[0]

    if len(idx) == 0:
        t_failure = np.nan
        rul_value = np.nan
    else:
        i = idx[0]
        t_failure = np.interp(
            g_threshold,
            [g[i-1], g[i]],
            [time[i-1], time[i]]
        )
        rul_value = t_failure - t_i

    return {
        't_inspection': t_i,
        't_failure': t_failure,
        'RUL': rul_value,
        'g_at_inspection': g_ti
    }


def g_emulator_at_inspect_time(bds, t_i, g_col="g_emulator"):
    """
    Retorna os valores de g_emulator exatamente no tempo t_i.
    Assume que t_i existe no dataset.
    """
    g_vals_ins = bds.loc[bds["time"] == t_i, g_col].values

    if len(g_vals_ins) == 0:
        raise ValueError(f"Time t_i = {t_i} not found in dataset.")

    return g_vals_ins


def g_emulator_at_limit_time(bds, t_limit, g_col="g_emulator"):
    """
    Retorna os valores de g_emulator exatamente no tempo limite t_limit.
    Assume que t_limit existe no dataset.
    """
    g_vals_lim = bds.loc[bds["time"] == t_limit, g_col].values

    if len(g_vals_lim) == 0:
        raise ValueError(f"Limit time t_limit = {t_limit} not found in dataset.")

    return g_vals_lim


# Beam class
class Beam():
    def __init__(self, geo: dict, mat: dict, load: dict, expo: dict):  
        """Initializes a Beam object with geometric, material, load, and exposure properties.
        
        :param geo: Geometric properties of the beam. Empty in this context
        :param mat: Material properties of the beam. Expected keys: 'f_ck [kPa]' - concrete compressive strength, 'Type of cement' - type of cement (0: CPII Z, 1: CPV-ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
        :param load: Load properties of the beam. Empty in this context
        :param expo: Exposure conditions for carbonation. Expected keys: 'Installation year' - year of installation, 'Exposure conditions' - exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected]), and 'Relative humidity [%]' - relative humidity
        """

        self.geo  = geo
        self.mat  = mat
        self.load = load
        self.expo = expo

    def latent_variable_generator(self, n_latent_samples: int) -> list:
        """Generates latent variables related the beam problem.

        :param n_latent_samples: Number of latent samples to generate.

        :return: Arrays of sampled relative humidity and concrete compressive strength deviations.
        """

        rh_mean = 1.0
        cov_rh  = 0.02
        sigma   = np.sqrt(np.log(1 + cov_rh**2))
        mu      = np.log(rh_mean) - sigma**2 / 2
        rh_beam = np.random.lognormal(mean=mu, sigma=sigma, size=n_latent_samples)
        
        fck_mean      = 1.0
        cov_fck       = 0.10
        fck_deviation = np.random.normal(loc=fck_mean, scale=cov_fck*fck_mean, size=n_latent_samples)
        
        return [rh_beam, fck_deviation]

class CO2Predictor:
    """Predictor for historical and modern atmospheric CO2 concentrations.   
    """

    def __init__(self, beam: Optional[Any] = None):
        """Initialize CO2Predictor with beam properties.
        
        :param beam: Beam object containing exposure and material properties
        """
        self.beam = beam
    
    def set_beam(self, beam: Any):
        """Set or update the beam properties."""
        self.beam = beam

    @staticmethod
    def co2_percentage_1900_1950(year: int) -> float:
        """CO2 atmospheric concentration (%) for historical period 1900–1950. Based on a linear approximation of the upward trend during this period.
        
        :param year: Calendar year (1900 <= year <= 1950)

        :return: CO2 concentration in percentage (ppm / 10000)
        """

        if not 1900 <= year <= 1950:
            raise ValueError("Year must be between 1900 and 1950 for this method.")
            
        co2_ppm = 296.0 + 0.30 * (year - 1900)
        return co2_ppm / 1e4

    @staticmethod
    def co2_percentage_1950_2000(year: int) -> float:
        """CO2 atmospheric concentration (%) for historical period 1950–2000. Based on a linear approximation of the accelerating upward trend.
        
        :param year: Calendar year (1950 <= year <= 2000)

        :return: CO2 concentration in percentage (ppm / 10000)
        """
        if not 1950 <= year <= 2000:
            raise ValueError("Year must be between 1950 and 2000 for this method.")
            
        co2_ppm = 311.0 + 1.16 * (year - 1950)
        return co2_ppm / 1e4

    @staticmethod
    def co2_percentage_pos2000(year: int) -> float:
        """CO2 atmospheric concentration (%) for post-2000 period. Captures the non-linear (quadratic) acceleration in CO2 buildup observed in recent decades.
        
        :param year: Calendar year (>= 2000)

        :return: CO2 concentration in percentage (ppm / 10000)
        """
        if year < 2000:
            raise ValueError("Year must be >= 2000 for this method.")
            
        t  = year - 2000
        C0 = 369.0   # ppm in 2000 (approximate observed value)
        a  = 1.85    # ppm/year (linear component)
        b  = 0.018   # ppm/year² (quadratic component)
        co2_ppm = C0 + a * t + b * t**2
        
        return co2_ppm / 1e4

    def co2_percentage_year(self, year: int) -> float:
        """Global average atmospheric CO2 concentration (%) valid from 1900 onwards. Routes the calculation to the correct historical formula based on the year.
        
        :param year: Calendar year (>= 1900)

        :return: CO2 concentration in percentage (ppm / 10000)
        """
        if year < 1900:
            raise ValueError(f"Year must be >= 1900. Received: {year}")

        if year <= 1950:
            return self.co2_percentage_1900_1950(year)
        elif 1950 < year <= 2000:
            return self.co2_percentage_1950_2000(year)
        else:
            return self.co2_percentage_pos2000(year)
        
    def carbonation_profile(self, model: Any, lifetime: float) -> pd.DataFrame:
        """Generate carbonation profile starting at a given calendar year.

        :param model: trained ML model for carbonation depth prediction, which should have a method .predict() and an attribute .feature_names_in_ that contains the names of the features used for training.
        :param lifetime: Design life of the structure [years]

        :return: DataFrame with columns C02 concentration (%), compressive strength (MPa), relative humidity (%), type of cement, exposure conditions, year, and carbonation depth (mm)
        """
        if self.beam is None:
            raise ValueError("Beam not set. Use set_beam() or pass beam to constructor.")

        start_year  = self.beam.expo['Installation year']
        rh          = self.beam.expo['Relative humidity [%]']
        exposure    = self.beam.expo['Exposure conditions']
        fc          = self.beam.mat['f_ck [kPa]'] / 1E3
        cement_type = self.beam.mat['Type of cement']

        # Time steps
        years = np.arange(0, lifetime + 1,10)

        # Romain calendar
        calendar_years = start_year + years

        # CO2 emission
        co2_values = [self.co2_percentage_year(y) for y in calendar_years]
   
        # Carbonation AI model and profile
        df      = pd.DataFrame({'t (years)': years, 'CO2 (%)': co2_values, 'fc (MPa)': [fc]*len(years), 'RH (%)': [rh]*len(years), 'Type of cement': [cement_type]*len(years), 'Exposure conditions': [exposure]*len(years)})
        df      = df[model.feature_names_in_]
        depth   = model.predict(df)
        profile = pd.DataFrame({'calendar year': calendar_years, 't (years)': years, 'CO2 (%)': co2_values, 'carbonation depth (mm)': depth})
        profile['carbonation depth (mm)'] = profile['carbonation depth (mm)'].cummax()

        return profile

    def carbonation_depth_at_time(self, profile: pd.DataFrame, t_query: float) -> float:
        """Returns carbonation depth at a specific time.

        :param profile : DataFrame with columns ['calendar year', 'carbonation depth (mm)']
        :param t_query : Calendar year for which to query the carbonation depth

        :return: Carbonation depth at the specified calendar year
        """

        t     = profile['calendar year'].values
        depth = profile['carbonation depth (mm)'].values

        return float(np.interp(t_query, t, depth))


def emulator_function_time_durability(
                                            x: np.ndarray, names_x_variables: list, carb_model: Any, 
                                            cement_type: int = 3, installation_year: int = 1990, exposure_conditions: int = 2,
                                            time_step: float = 0.0, n_latent_samples: int = 1000, verbose: bool = False
                                        ) -> pd.DataFrame:
    """Compute the emulator of carbonation depth for durability analysis of reinforced concrete sections. 
    """
    
    dfs = []
    predictor = CO2Predictor()  # Create predictor instance (sem beam ainda)

    for i in range(x.shape[0]):
        # =========================
        # 1. Beam properties (durability analysis)
        # =========================
        mat = {
                'f_ck [kPa]': float(x[i][0]),
                'Type of cement': cement_type
              }
        expo = {
                 'Installation year': installation_year,
                 'Exposure conditions': exposure_conditions,
                 'Relative humidity [%]': float(x[i][1])
               }
        geo, load = {}, {}


        # =========================
        # 2. Generate latent variables (humidity uncertainty)
        # =========================
        base_rh       = expo['Relative humidity [%]']
        base_fck      = mat['f_ck [kPa]']
        beam_instance = Beam(geo=geo, mat=mat, load=load, expo=expo)
        res        = beam_instance.latent_variable_generator(n_latent_samples)
        rh_latent  = np.array(res[0]).flatten()
        fck_latent = np.array(res[1]).flatten()
        
        # =========================
        # 3. Carbonation analysis for each latent humidity sample
        # =========================
        carbonation_depths = np.zeros(n_latent_samples)
        start_year = installation_year
        year_query = start_year + time_step
        
        for j in range(n_latent_samples):
            # Apply latent variable to humidity
            expo_with_rh = expo.copy()
            mat_with_fck = mat.copy()
            new_rh       = expo['Relative humidity [%]'] * rh_latent[j]
            new_fck      = mat['f_ck [kPa]'] * fck_latent[j]
            
            # Ensure humidity is within physical limits
            if new_rh > 100:
                new_rh = 100
            elif new_rh < 0:
                new_rh = 0
                
            if new_fck < 0:
                new_fck = 0
            
            expo_with_rh['Relative humidity [%]'] = new_rh
            mat_with_fck['f_ck [kPa]']            = new_fck
            
            # Create beam with updated humidity
            beam_with_rh = Beam(geo=geo, mat=mat_with_fck, load=load, expo=expo_with_rh)
            
            # Generate carbonation profile
            predictor.set_beam(beam_with_rh)
            profile = predictor.carbonation_profile(model=carb_model, lifetime=time_step)
            
            # Calculate carbonation depth
            carb_depth_mm = predictor.carbonation_depth_at_time(profile, year_query)
            
            if carb_depth_mm < 0:
                carb_depth_mm = 0.0
            
            carbonation_depths[j] = carb_depth_mm

        # =========================
        # 4. Emulator of carbonation depth
        # =========================
        g_vals = carbonation_depths
        
        # =========================
        # 5. Create DataFrame
        # =========================
        df = pd.DataFrame({
                            names_x_variables[0]: [x[i, 0]] * n_latent_samples,
                            names_x_variables[1]: [x[i, 1]] * n_latent_samples,
                            'RH_latent': rh_latent,
                            'RH_effective': [base_rh * r for r in rh_latent],
                            'FCK_latent': fck_latent,
                            'FCK_effective': [base_fck * f for f in fck_latent],
                            'Carbonation_depth_mm': carbonation_depths,
                            'Time (years)': time_step,
                            'g': g_vals
                        })

        # =========================
        # 6. GLAM fitting
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

        dfs.append(df)
        
        if verbose:
            print(f"  Sample {i+1}:")
            print(f"    P(g < 0) = {np.mean(g_vals < 0):.4f}")
            print(f"    Mean carbonation depth = {np.mean(carbonation_depths):.2f} mm")

    return pd.concat(dfs, ignore_index=True)