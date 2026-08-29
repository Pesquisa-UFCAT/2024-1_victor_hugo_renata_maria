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


# def state_limit_function(x: np.ndarray, n_latent_samples: int) -> tuple[np.ndarray, pd.DataFrame]:
#     """State limit function with time effect. Considering Z_1 and Z_2 are the latent variables.
    
#     :param x: Input variables [0] = Resistance R ; [1] = Load S
#     :param n_latent_samples: Number of latent samples to be generated for each input sample
    
#     :return: [0] = GLAM parameters ; [1] = Dataset with Resitance 'r', Load 's', latent variables 'z1' and 'z2', and state limit function 'g'
#     """
    
#     y_aux = []
#     dfs = []
#     for i in range(x.shape[0]):
#         df = {'r': [x[i, 0]] * n_latent_samples, 's': [x[i, 1]] * n_latent_samples}
#         df = pd.DataFrame(df)
#         z1aux = []
#         z2aux = []
#         for i in df.iterrows():
#             z1_mu = 1.
#             z1_sc = 0.028
#             s = np.sqrt(np.log(1 + (z1_sc/z1_mu)**2))
#             scale = z1_mu / np.sqrt(1 + (z1_sc/z1_mu)**2)
#             z1aux.append(stats.lognorm.rvs(s=s, scale=scale, size=1)[0])
#             z2_mu = 1.
#             z2_sc = 0.096
#             s = np.sqrt(np.log(1 + (z2_sc/z2_mu)**2))
#             scale = z2_mu / np.sqrt(1 + (z2_sc/z2_mu)**2)
#             z2aux.append(stats.lognorm.rvs(s=s, scale=scale, size=1)[0])
#         df['z1'] = z1aux
#         df['z2'] = z2aux
#         df['g'] = df['r']/df['z1'] - df['s'] * df['z2']
#         dfs.append(df)
#         lambdas, _ = fit_gld_fkml_mle(df['g'].values)
#         y_aux.append(lambdas)
#         y = np.array(y_aux)
#     return y, dfs


def state_limit_function_time(x: np.ndarray, n_latent_samples: int, t: float = 0.0) -> tuple[np.ndarray, pd.DataFrame]:
    """State limit function with time effect. Considering Z_1 and Z_2 are the latent variables.
    
    :param x: Input variables [0] = Resistance R ; [1] = Load S
    :param n_latent_samples: Number of latent samples to be generated for each input sample
    :param t: Time parameter affecting the state limit function
    
    :return: [0] = GLAM parameters ; [1] = Dataset with Resitance 'r', Load 's', latent variables 'z1' and 'z2', and state limit function 'g'
    """
    
    y_aux = []
    dfs = []
    for i in range(x.shape[0]):
        df = {'r': [x[i, 0]] * n_latent_samples, 's': [x[i, 1]] * n_latent_samples}
        df = pd.DataFrame(df)
        z1aux = []
        z2aux = []
        for i in df.iterrows():
            z1_mu = 1.
            z1_sc = 0.028
            s = np.sqrt(np.log(1 + (z1_sc/z1_mu)**2))
            scale = z1_mu / np.sqrt(1 + (z1_sc/z1_mu)**2)
            z1aux.append(stats.lognorm.rvs(s=s, scale=scale, size=1)[0])
            z2_mu = 1.
            z2_sc = 0.096
            s = np.sqrt(np.log(1 + (z2_sc/z2_mu)**2))
            scale = z2_mu / np.sqrt(1 + (z2_sc/z2_mu)**2)
            z2aux.append(stats.lognorm.rvs(s=s, scale=scale, size=1)[0])
        df['z1'] = z1aux
        df['z2'] = z2aux
        k_factor = 1 + (0.3 - 1) * t / 100
        df['g'] = k_factor * df['r']/df['z1'] - df['s'] * df['z2']
        dfs.append(df)
        lambdas, _ = fit_gld_fkml_mle(df['g'].values)
        y_aux.append(lambdas)
        y = np.array(y_aux)
    
    return y, dfs


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
        
        :param geo: Geometric properties of the beam. Expected keys: 'cover [m]' - concrete cover
        :param mat: Material properties of the beam. Expected keys: 'f_ck [kPa]' - concrete compressive strength, 'Type of cement' - type of cement (0: CPII Z, 1: CPV -ARI, 2: CPIV, 3: CPII F, 4: CPIII, 5: CPII E)
        :param load: Load properties of the beam. 
        :param expo: Exposure conditions for carbonation. Expected keys: 'Installation year' - year of installation, 'Exposure conditions' - exposure conditions (0: PIA [Internal Protected], 1: UEA [External Unprotected], 2: PEA [External Protected]), and 'Relative humidity [%]' - relative humidity
        """

        self.geo = geo
        self.mat = mat
        self.load = load
        self.expo = expo

    def latent_variable_generator(self, n_latent_samples: int) -> list:
        """Generates latent variables related the beam problem.

        :param n_latent_samples: Number of latent samples to generate.

        :return: Arrays of sampled relative humidity.
        """

        rh_mean = 1.0
        cov_rh  = 0.05
        sigma   = np.sqrt(np.log(1 + cov_rh**2))
        mu      = np.log(rh_mean) - sigma**2 / 2
        rh_beam = np.random.lognormal(mean=mu, sigma=sigma, size=n_latent_samples)
        
        return [rh_beam]

    def co2_percentage_1900_1950(self, year) -> float:
        """CO2 atmospheric concentration (%) for the historical periods 1900–1950. 

        :param year: Calendar year for which to calculate the CO2 concentration

        :return: CO2 concentration in percentage (ppm / 1e4)
        """
        co2_ppm = 296.0 + 0.30 * (year - 1900)

        return co2_ppm / 1e4

    def co2_percentage_1950_2000(self, year) -> float:
        """CO2 atmospheric concentration (%) for the historical periods 1950–2000. 

        :param year: Calendar year for which to calculate the CO2 concentration

        :return: CO2 concentration in percentage (ppm / 1e4)
        """

        co2_ppm = 311.0 + 1.16 * (year - 1950)
        
        return co2_ppm / 1e4

    def co2_percentage_pos2000(self, year) -> float:
        """CO2 atmospheric concentration (%) for the historical periods post-2000.

        :param year: Calendar year for which to calculate the CO2 concentration

        :return: CO2 concentration in percentage (ppm / 1e4)
        """

        t = year - 2000

        C0 = 369.0   # ppm in 2000
        a  = 1.85    # ppm/year
        b  = 0.018   # ppm/year²
        co2_ppm = C0 + a * t + b * t**2

        return co2_ppm / 1e4

    def co2_percentage_year(self, year) -> float:
        """Global average atmospheric CO2 concentration (%) valid from 1900 onwards.

        :param year: Calendar year for which to calculate the CO2 concentration

        :return: CO2 concentration in percentage (ppm / 1e4)
        """

        if year <= 1950:
            return self.co2_percentage_1900_1950(year)
        elif 1950 < year <= 2000:
            return self.co2_percentage_1950_2000(year)
        else:
            return self.co2_percentage_pos2000(year)
        
    def carbonation_profile(self, model: Any, lifetime: float) -> pd.DataFrame:
        """Generate carbonation profile starting at a given calendar year."""
    
        start_year = self.expo['Installation year']
        rh = self.expo['Relative humidity [%]']
        exposure = self.expo['Exposure conditions']
        fc = self.mat['f_ck [kPa]'] / 1E3
        cement_type = self.mat['Type of cement']

        # Time steps
        years = np.arange(0, lifetime + 1, 10)
        
        # Romain calendar
        calendar_years = start_year + years

        # CO2 emission
        co2_values = [self.co2_percentage_year(y) for y in calendar_years]

        # Carbonation AI model and profile
        df = pd.DataFrame({
            't (years)': years, 
            'CO2 (%)': co2_values, 
            'fc (MPa)': [fc] * len(years), 
            'RH (%)': [rh] * len(years), 
            'Type of cement': [cement_type] * len(years), 
            'Exposure conditions': [exposure] * len(years)
        })
        df = df[model.feature_names_in_]
        depth = model.predict(df)
        
        # CORREÇÃO: Forçar profundidade zero no tempo zero
        depth = np.maximum(depth, 0)
        
        profile = pd.DataFrame({
            'calendar year': calendar_years, 
            't (years)': years, 
            'CO2 (%)': co2_values, 
            'carbonation depth (mm)': depth
        })
        profile['carbonation depth (mm)'] = profile['carbonation depth (mm)'].cummax()
        
        # Garantir que o primeiro ponto seja zero
        profile.loc[0, 'carbonation depth (mm)'] = 0.0
        
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


    def simple_support_beam_max_bending_moment(self, p_k: float) -> float:
        """Computes the bending moment at mid-span for a simply supported beam under a uniformly distributed load.

        :param p_k: Characteristic distributed load [kN/m]

        :return: Bending moment at mid-span [kNm]
        """

        return p_k * self.geo['l [m]']**2 / 8

    def design_bending_moment(self, g_k: float, q_k: float) -> float:
        """Computes the design bending moment for a simply supported beam under permanent and variable distributed loads.

        :param g_k: Permanent load [kN/m]
        :param q_k: Variable load [kN/m]

        :return: Design bending moment Sd [kNm] considering load partial safety factors
        """

        m_gk = self.simple_support_beam_max_bending_moment(p_k=g_k)
        m_qk = self.simple_support_beam_max_bending_moment(p_k=q_k)

        return self.load['gamma_g'] * m_gk + self.load['gamma_q'] * m_qk

    def f_alpha(self, a_st: float, beta: float) -> float:
        """Residual of the axial force equilibrium equation for a rectangular reinforced concrete section, using the simplified stress block of NBR 6118 (2023).

        :param a_st: Tensile steel area [m²]
        :param beta: Neutral axis ratio x/d

        :return: Residual of force equilibrium (concrete – steel)
        """

        # Concrete parameters
        if self.mat['f_ck [kPa]'] > 50000:
            lambda_c   = 0.80 - ((self.mat['f_ck [kPa]']/1000) - 50) / 400
            alpha_c    = (1.00 - ((self.mat['f_ck [kPa]']/1000) - 50) / 200) * 0.85
            eta_c      = (40 / (self.mat['f_ck [kPa]']/1000)) ** (1/3)
            epsilon_cu = 2.6e-3 + 35e-3 * ((90 - self.mat['f_ck [kPa]']/1000) / 100) ** 4
        else:
            lambda_c   = 0.80
            alpha_c    = 0.85
            eta_c      = 1.00
            epsilon_cu = 3.5e-3

        # Concrete stress block
        f_cd     = self.mat['f_ck [kPa]'] / self.mat['gamma_c']
        sigma_cd = alpha_c * eta_c * f_cd

        # Neutral axis depth
        x = beta *  (self.geo['h [m]'] * self.geo['ratio d/h'])

        # Resultant concrete force
        r_cc = sigma_cd * lambda_c * x * self.geo['b_w [m]']

        # Domain limit between 2 and 3
        beta_lim = epsilon_cu / (epsilon_cu + 10e-3)

        # Steel strain
        if beta <= beta_lim:
            epsilon_st = 10e-3
        else:
            epsilon_st = epsilon_cu * (1 - beta) / beta

        # Steel stress
        f_yd       = self.mat['f_yk [kPa]'] / self.mat['gamma_s']
        epsilon_yd = f_yd / self.mat['e_s [kPa]']

        if abs(epsilon_st) <= epsilon_yd:
            sigma_st = self.mat['e_s [kPa]'] * epsilon_st
        else:
            sigma_st = np.sign(epsilon_st) * f_yd

        # Resultant steel force
        r_st = sigma_st * a_st

        return r_cc - r_st
    
    def design_resistant_bending_moment_without_corrosion(self, a_st: float) -> float:
        """Computes the design resistant bending moment for a simply supported beam under permanent and variable distributed loads.

        :param a_st: Tensile steel area [m²]
        
        :return: Design resistant bending moment Rd [kNm]
        """

        # Concrete parameters
        if self.mat['f_ck [kPa]'] > 50000:
            lambda_c = 0.80 - ((self.mat['f_ck [kPa]']/1000) - 50) / 400
            alpha_c  = (1.00 - ((self.mat['f_ck [kPa]']/1000) - 50) / 200) * 0.85
            eta_c    = (40 / (self.mat['f_ck [kPa]']/1000)) ** (1/3)
        else:
            lambda_c = 0.80
            alpha_c  = 0.85
            eta_c    = 1.00

        # Axial force equilibrium to find neutral axis depth
        d   = self.geo['h [m]'] * self.geo['ratio d/h']
        sol = sc.optimize.root_scalar(lambda beta: self.f_alpha(a_st=a_st, beta=beta), bracket=(1e-5, d / self.geo['h [m]']), method='bisect')
        x   = sol.root * d

        # Resistant moment
        f_cd     = self.mat['f_ck [kPa]'] / self.mat['gamma_c']
        sigma_cd = alpha_c * eta_c * f_cd
        r_cc     = sigma_cd * lambda_c * x * self.geo['b_w [m]']
        
        return r_cc * (d - 0.5 * lambda_c * x)

    def corrosion_index(self, temp: float) -> float:
        """Determines the corrosion index of steel reinforcements in reinforced concrete considering the influence of ambient temperature on the corrosion rate, according to Peng and Stewart (2016).

        :param temp: Temperature of the environment (°C)

        :return: Adjusted corrosion index [μA/cm²]
        """

        # Correção para temperaturas diferentes de 20°C
        if temp > 20:
            k = 0.073
        elif temp < 20:
            k = 0.025
        elif temp == 20:
            k = 0
        i_corr = self.expo['i_corr_20'] * (1 + k * (temp - 20))

        return i_corr

    def design_resistant_bending_moment_with_corrosion(self, t: float, t_carb: float, temp: float) -> float:
        """Computes the design resistant bending moment for a simply supported beam under permanent and variable distributed loads considering corrosion effects.

        :param t: Time elapsed since the structure was built [year]
        :param t_carb: Time for carbonation to reach the reinforcement [year]
        :param temp: Temperature of the environment (°C)

        :return: Design resistant bending moment Rd [kNm] with corrosion effects
        """

        # Corrosion parameters
        delta_time_cor = max(0.0, t - t_carb)
        i_corr_uA      = self.corrosion_index(temp)

        # Loss of diameter (Al-Gohi model)
        d_0_mm    = self.geo['phi [m]'] * 1000
        delta_dim = 0.0232 * i_corr_uA * delta_time_cor
        d_cor     = max(0.0, (d_0_mm - delta_dim) / 1000)
        a_s_cor   = self.geo['n bars'] * (np.pi * d_cor**2 / 4)
        
        # Resistant moment
        if delta_time_cor == 0:
            c_f = 1.0
        else:
            i_corr_mA = i_corr_uA / 1000
            cf_aux    = 5 / (d_0_mm ** 0.54 * (i_corr_mA * delta_time_cor * 365) ** 0.19)
            c_f       = min(1.0, cf_aux)
        m_raux = self.design_resistant_bending_moment_without_corrosion(a_st=a_s_cor)
        
        return m_raux * c_f


def state_limit_function_time_structural(
    x: np.ndarray,
    names_x_variables: list,
    carb_model: Any,
    beam_ref: Any,
    time_step: float,
    n_latent_samples: int,
    lifetime_max: float = 100,
    verbose: bool = False
) -> pd.DataFrame:
    """
    Compute structural limit state function with carbonation effects and 
    corrosion propagation, with full uncertainty propagation.
    """
    
    dfs = []

    for i in range(x.shape[0]):
        if verbose:
            print(f"Processing sample {i+1}/{x.shape[0]}")

        # =========================
        # 1. Atualizar propriedades da viga
        # =========================
        geo = beam_ref.geo.copy()
        mat = beam_ref.mat.copy()
        load = beam_ref.load.copy()
        expo = beam_ref.expo.copy()

        geo['cover [m]'] = float(x[i][0])
        mat['f_ck [kPa]'] = float(x[i][1])
        expo['Relative humidity [%]'] = float(x[i][2])
        
        # Guardar umidade base para multiplicação
        base_rh = expo['Relative humidity [%]']

        # =========================
        # 2. Gerar variáveis latentes de umidade (propagação de incertezas)
        # =========================
        beam_temp = Beam(geo=geo, mat=mat, load=load, expo=expo)
        rh_latent = beam_temp.latent_variable_generator(n_latent_samples)
        rh_latent = np.array(rh_latent).flatten()
        
        # =========================
        # 3. Carbonatação para cada amostra latente de umidade
        # =========================
        carbonation_depths = np.zeros(n_latent_samples)
        carbonation_times = np.full(n_latent_samples, lifetime_max)  # Default: nunca atinge
        
        cover_mm = geo['cover [m]'] * 1e3
        start_year = expo['Installation year']
        year_query = start_year + time_step
        
        # Discretização adaptativa para busca do tempo de iniciação
        if time_step > 0:
            n_points = min(100, int(lifetime_max) + 1)
            search_times = np.linspace(0, time_step, n_points)
        else:
            search_times = np.array([0.0])
        
        for j in range(n_latent_samples):
            # CORREÇÃO: Multiplicar umidade base pelo fator latente
            expo_with_rh = expo.copy()
            new_rh = base_rh * rh_latent[j]
            
            # Garantir que a umidade fique dentro de limites físicos (0-100%)
            if new_rh > 100:
                new_rh = 100
            elif new_rh < 0:
                new_rh = 0
            
            expo_with_rh['Relative humidity [%]'] = new_rh
            
            # Criar beam com umidade atualizada
            beam_with_rh = Beam(geo=geo, mat=mat, load=load, expo=expo_with_rh)
            
            # Gerar perfil de carbonatação completo
            profile = beam_with_rh.carbonation_profile(model=carb_model, lifetime=lifetime_max)
            
            # O modelo já retorna em mm
            carb_depth_mm = beam_with_rh.carbonation_depth_at_time(profile, year_query)
            
            # Garantir que não seja negativo
            if carb_depth_mm < 0:
                if verbose:
                    print(f"    Aviso: profundidade negativa detectada ({carb_depth_mm:.2f} mm), ajustando para 0")
                carb_depth_mm = 0.0
            
            carbonation_depths[j] = carb_depth_mm
            
            # Calcular tempo de iniciação da corrosão
            if carb_depth_mm >= cover_mm:
                # Se já atingiu, encontrar tempo exato com interpolação
                for idx, tau in enumerate(search_times):
                    year_tau = start_year + tau
                    depth_tau_mm = beam_with_rh.carbonation_depth_at_time(profile, year_tau)
                    
                    # Garantir que não seja negativo
                    if depth_tau_mm < 0:
                        depth_tau_mm = 0.0
                    
                    if depth_tau_mm >= cover_mm:
                        if idx > 0:
                            # Interpolação linear entre os dois pontos
                            tau_prev = search_times[idx-1]
                            depth_prev_mm = beam_with_rh.carbonation_depth_at_time(profile, start_year + tau_prev)
                            
                            if depth_prev_mm < 0:
                                depth_prev_mm = 0.0
                            
                            if depth_prev_mm < cover_mm:
                                t_carb = tau_prev + (cover_mm - depth_prev_mm) * (tau - tau_prev) / (depth_tau_mm - depth_prev_mm)
                            else:
                                t_carb = tau
                        else:
                            t_carb = tau
                        carbonation_times[j] = t_carb
                        break
            else:
                # Buscar tempo de iniciação após o tempo atual
                future_times = np.linspace(time_step, lifetime_max, min(100, int(lifetime_max - time_step) + 1))
                all_search_times = np.concatenate([search_times, future_times])
                for tau in all_search_times:
                    year_tau = start_year + tau
                    depth_tau_mm = beam_with_rh.carbonation_depth_at_time(profile, year_tau)
                    
                    if depth_tau_mm < 0:
                        depth_tau_mm = 0.0
                    
                    if depth_tau_mm >= cover_mm:
                        carbonation_times[j] = tau
                        break

        # =========================
        # 4. Amostragem latente estrutural (fatores de incerteza)
        # =========================
        theta_R = np.random.lognormal(mean=0.0, sigma=0.05, size=n_latent_samples)
        theta_S = np.random.lognormal(mean=0.0, sigma=0.10, size=n_latent_samples)

        # =========================
        # 5. Resistência com corrosão
        # =========================
        R_vals = np.zeros(n_latent_samples)
        
        # Parâmetros de carga
        g_k = load.get('g_k [kN/m]', 5.0)
        q_k = load.get('q_k [kN/m]', 2.0)
        S_base = beam_ref.design_bending_moment(g_k=g_k, q_k=q_k)
        S_vals = S_base * theta_S

        for j in range(n_latent_samples):
            # Calcular resistência considerando corrosão no tempo atual
            R = beam_ref.design_resistant_bending_moment_with_corrosion(
                t=time_step,
                t_carb=carbonation_times[j],
                temp=expo.get('temp [°C]', 20.0)
            )
            R_vals[j] = R * theta_R[j]

        # =========================
        # 6. Estado limite
        # =========================
        g_vals = R_vals - S_vals

        # =========================
        # 7. Criar DataFrame com resultados
        # =========================
        df = pd.DataFrame({
            names_x_variables[0]: [x[i, 0]] * n_latent_samples,
            names_x_variables[1]: [x[i, 1]] * n_latent_samples,
            names_x_variables[2]: [x[i, 2]] * n_latent_samples,
            'RH_latent': rh_latent,
            'RH_effective': [base_rh * r for r in rh_latent],  # Umidade efetiva após multiplicação
            'Carbonation_depth_mm': carbonation_depths,
            'Carbonation_time_years': carbonation_times,
            'Time (years)': time_step,
            'R': R_vals,
            'S': S_vals,
            'g': g_vals
        })

        # =========================
        # 8. GLAM fitting com tratamento de erro robusto
        # =========================
        try:
            emulator = glam.GlamFKML()
            sol = emulator.fit_lambdas(df['g'].values, method="least_squares")
            if sol.success:
                lambdas = sol.x
            else:
                lambdas = [np.nan] * 4
        except Exception as e:
            if verbose:
                print(f"GLAM fitting failed for sample {i}: {e}")
            lambdas = [np.nan] * 4

        df['lambda 1'] = lambdas[0]
        df['lambda 2'] = lambdas[1]
        df['lambda 3'] = lambdas[2]
        df['lambda 4'] = lambdas[3]

        dfs.append(df)
        
        if verbose:
            # Estatísticas para monitoramento
            print(f"  Sample {i+1}:")
            print(f"    P(g < 0) = {np.mean(g_vals < 0):.4f}")
            print(f"    Mean carbonation depth = {np.mean(carbonation_depths):.2f} mm")
            print(f"    Mean initiation time = {np.mean(carbonation_times):.2f} years")
            n_reached = np.sum(carbonation_times < lifetime_max)
            print(f"    Samples that reached cover: {n_reached}/{n_latent_samples} ({100*n_reached/n_latent_samples:.1f}%)")
            print(f"    GLAM converged: {sol.success if 'sol' in locals() else False}")

    return pd.concat(dfs, ignore_index=True)


def get_carbonation_statistics(beam_instance, n_samples=1000, time_step=50, lifetime_max=100):
    """
    Calcula estatísticas de carbonatação para um beam específico,
    considerando incertezas nas variáveis latentes.
    
    :param beam_instance: Instância da classe Beam
    :param n_samples: Número de amostras latentes
    :param time_step: Tempo de avaliação
    :param lifetime_max: Vida útil máxima
    :return: Dicionário com estatísticas
    """
    
    rh_latent = beam_instance.latent_variable_generator(n_samples)
    rh_latent = np.array(rh_latent).flatten()
    
    depths = []
    times_to_cover = []
    
    start_year = beam_instance.expo['Installation year']
    cover_mm = beam_instance.geo['cover [m]'] * 1e3
    
    for rh in rh_latent:
        expo_copy = beam_instance.expo.copy()
        expo_copy['Relative humidity [%]'] = rh
        
        beam_rh = Beam(
            geo=beam_instance.geo,
            mat=beam_instance.mat,
            load=beam_instance.load,
            expo=expo_copy
        )
        
        profile = beam_rh.carbonation_profile(model=carb_model, lifetime=lifetime_max)
        
        year_query = start_year + time_step
        depth = beam_rh.carbonation_depth_at_time(profile, year_query)
        depths.append(depth)
        
        # Encontrar tempo para atingir a cobertura
        t_carb = lifetime_max
        for tau in np.linspace(0, lifetime_max, 200):
            year_tau = start_year + tau
            if beam_rh.carbonation_depth_at_time(profile, year_tau) >= cover_mm:
                t_carb = tau
                break
        times_to_cover.append(t_carb)
    
    return {
        'depth_mean': np.mean(depths),
        'depth_std': np.std(depths),
        'depth_percentiles': np.percentile(depths, [5, 50, 95]),
        'time_mean': np.mean(times_to_cover),
        'time_std': np.std(times_to_cover),
        'time_percentiles': np.percentile(times_to_cover, [5, 50, 95])
    }


# No arquivo functions_.py, após a função state_limit_function_time_structural
# e antes do final do arquivo, adicione:

def validate_results(results, x_samples, lifetime_max=100):
    """
    Valida os resultados e gera estatísticas resumidas.
    
    :param results: Dicionário com resultados por tempo (output de state_limit_function_time_structural)
    :param x_samples: Matriz de amostras de entrada
    :param lifetime_max: Vida útil máxima para filtrar tempos de iniciação
    """
    
    print("\n" + "="*60)
    print("VALIDAÇÃO DOS RESULTADOS")
    print("="*60)
    
    for t, df in results.items():
        print(f"\n{'='*40}")
        print(f"TEMPO: {t} anos")
        print(f"{'='*40}")
        print(f"  Número de amostras totais: {len(df)}")
        print(f"  Probabilidade de falha P(g < 0): {np.mean(df['g'] < 0):.4f}")
        print(f"  g - média: {df['g'].mean():.4f}")
        print(f"  g - desvio padrão: {df['g'].std():.4f}")
        print(f"  g - mínimo: {df['g'].min():.4f}")
        print(f"  g - máximo: {df['g'].max():.4f}")
        print(f"  R - média: {df['R'].mean():.4f}")
        print(f"  S - média: {df['S'].mean():.4f}")
        
        # Verificar carbonation_times se existir
        if 'Carbonation_time_years' in df.columns:
            valid_times = df['Carbonation_time_years'] < lifetime_max
            n_valid = valid_times.sum()
            n_invalid = len(df) - n_valid
            
            print(f"\n  ANÁLISE DE CARBONATAÇÃO:")
            print(f"    Amostras que atingiram a armadura: {n_valid} ({100*n_valid/len(df):.1f}%)")
            print(f"    Amostras que NÃO atingiram: {n_invalid} ({100*n_invalid/len(df):.1f}%)")
            
            if n_valid > 0:
                print(f"    Tempo de iniciação - média: {df['Carbonation_time_years'][valid_times].mean():.2f} anos")
                print(f"    Tempo de iniciação - desvio: {df['Carbonation_time_years'][valid_times].std():.2f} anos")
                print(f"    Tempo de iniciação - percentis (5%, 50%, 95%): "
                      f"{np.percentile(df['Carbonation_time_years'][valid_times], [5, 50, 95])}")
            
            print(f"    Profundidade carbonatação - média: {df['Carbonation_depth_mm'].mean():.2f} mm")
            print(f"    Profundidade carbonatação - desvio: {df['Carbonation_depth_mm'].std():.2f} mm")
        
        # Verificar lambdas
        lambda_cols = ['lambda 1', 'lambda 2', 'lambda 3', 'lambda 4']
        if all(col in df.columns for col in lambda_cols):
            print(f"\n  PARÂMETROS GLAM (média):")
            for col in lambda_cols:
                # Ignorar NaNs se houver
                valid_lam = df[col][~np.isnan(df[col])]
                if len(valid_lam) > 0:
                    print(f"    {col}: {valid_lam.mean():.4f} ± {valid_lam.std():.4f}")
                else:
                    print(f"    {col}: NaN")
    
    # Análise geral
    print("\n" + "="*60)
    print("RESUMO GERAL")
    print("="*60)
    
    tempos = sorted(results.keys())
    prob_falha = [np.mean(results[t]['g'] < 0) for t in tempos]
    
    print("\nEvolução da probabilidade de falha:")
    for t, pf in zip(tempos, prob_falha):
        print(f"  t = {t:3d} anos: P(falha) = {pf:.4f}")
    
    # Identificar quando a probabilidade de falha ultrapassa 5% e 10%
    limiar_5 = None
    limiar_10 = None
    for t, pf in zip(tempos, prob_falha):
        if limiar_5 is None and pf >= 0.05:
            limiar_5 = t
        if limiar_10 is None and pf >= 0.10:
            limiar_10 = t
    
    if limiar_5:
        print(f"\nTempo para P(falha) >= 5%: {limiar_5} anos")
    if limiar_10:
        print(f"Tempo para P(falha) >= 10%: {limiar_10} anos")
    
    return {
        'tempos': tempos,
        'prob_falha': prob_falha,
        'limiar_5': limiar_5,
        'limiar_10': limiar_10
    }