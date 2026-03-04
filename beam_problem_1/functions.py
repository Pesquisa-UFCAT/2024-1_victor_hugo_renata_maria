import os
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
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import scipy.stats as stats
from multiprocessing import Pool, cpu_count
from scipy.interpolate import interp1d
import scipy as sc
import joblib


def find_excel_file(filename, max_depth=5):
    """Busca o arquivo Excel em 5 diretórios acima e 5 diretórios abaixo
    """
    
    # Começa do diretório atual
    current_dir = Path.cwd()
    
    # Procura para cima (diretórios pais)
    for i in range(max_depth):
        search_dir = current_dir
        # Procura em todas as pastas do diretório atual
        for root, dirs, files in os.walk(search_dir):
            if filename in files:
                return os.path.join(root, filename)
        
        # Sobe um nível
        current_dir = current_dir.parent
        
        # Se chegou na raiz, para
        if current_dir == current_dir.parent:
            break
    
    return None


# ================= FKML: núcleo matemático =================
def _phi(u, lam):
    # Trata lam -> 0 por continuidade: (u^lam - 1)/lam -> ln(u)
    return np.where(np.isclose(lam, 0.0), np.log(u), (u**lam - 1.0)/lam)

def gld_fkml_quantile(u, l1, l2, l3, l4):
    u = np.clip(u, 1e-12, 1-1e-12)
    return l1 + ( _phi(u, l3) - _phi(1-u, l4) ) / l2

def gld_fkml_qprime(u, l2, l3, l4):
    # Q'(u) = (u^(l3-1) + (1-u)^(l4-1)) / l2, com limites log quando lam≈0
    u = np.clip(u, 1e-12, 1-1e-12)
    term1 = np.where(np.isclose(l3, 0.0), 1.0/u, u**(l3 - 1.0))
    term2 = np.where(np.isclose(l4, 0.0), 1.0/(1.0 - u), (1.0 - u)**(l4 - 1.0))
    return (term1 + term2) / l2

# Newton estável para resolver x = Q(u)
def _solve_u_for_x(x, l1, l2, l3, l4, maxit=60, tol=1e-10):
    x = np.atleast_1d(x).astype(float)
    # chute inicial por ranking -> (0,1)
    ranks = (np.argsort(np.argsort(x)) + 0.5) / (len(x) + 1.0)
    u = np.clip(ranks, 1e-4, 1-1e-4)
    for _ in range(maxit):
        q  = gld_fkml_quantile(u, l1, l2, l3, l4)
        qp = gld_fkml_qprime(u, l2, l3, l4)
        step = (q - x)/np.maximum(qp, 1e-16)
        u_new = np.clip(u - step, 1e-8, 1-1e-8)
        if np.max(np.abs(u_new - u)) < tol:
            u = u_new
            break
        u = u_new
    return u

def gld_fkml_pdf(x, l1, l2, l3, l4):
    if l2 <= 0:
        return np.full_like(np.atleast_1d(x), 0.0, dtype=float)
    u  = _solve_u_for_x(x, l1, l2, l3, l4)
    qp = gld_fkml_qprime(u, l2, l3, l4)
    return 1.0/np.maximum(qp, 1e-300)

# ================= MLE com bounds e padronização =================
def _mad(x):
    med = np.median(x)
    return np.median(np.abs(x - med))

def fit_gld_fkml_mle(data, x0=None, bounds=None):
    data = np.asarray(data, dtype=float)
    # Padroniza para estabilizar a busca
    m, s = np.median(data), (1.4826*_mad(data) or np.std(data, ddof=1) or 1.0)
    z = (data - m)/s

    # inicialização
    if x0 is None:
        x0 = np.array([0.0, 1.0, 0.1, 0.1])  # l1≈0, l2≈1, leve assimetria

    # bounds: l2>0; restringe forma para evitar explosões numéricas
    if bounds is None:
        bounds = [(-np.inf, np.inf), (1e-4, np.inf), (-3.0, 3.0), (-3.0, 3.0)]

    def nll(params):
        l1, l2, l3, l4 = params
        if not np.isfinite(l1 + l2 + l3 + l4) or l2 <= 0:
            return np.inf
        f = gld_fkml_pdf(z, l1, l2, l3, l4)
        if np.any(f <= 0) or np.any(~np.isfinite(f)):
            return np.inf
        return -np.sum(np.log(f))

    res = minimize(nll, x0, method="L-BFGS-B", bounds=bounds)

    # desfaz padronização: Qx(u) = m + s * Qz(u)  => l1x = m + s*l1z ; l2x = l2z / s
    l1z, l2z, l3, l4 = res.x
    l1x = m + s*l1z
    l2x = l2z / s
    return (l1x, l2x, l3, l4), res

# ================= Plot APENAS da GLD =================
def plot_gld_only(lambdas, n_points=2000, quantile_trim=1e-3, qp_min=1e-8, ylim=None):
    l1, l2, l3, l4 = lambdas
    a = float(quantile_trim)
    u = np.linspace(a, 1.0 - a, n_points)
    x = gld_fkml_quantile(u, l1, l2, l3, l4)
    qp = gld_fkml_qprime(u, l2, l3, l4)

    mask = np.isfinite(x) & np.isfinite(qp) & (qp > qp_min)
    x, f = x[mask], (1.0/qp[mask])

    order = np.argsort(x)
    x, f = x[order], f[order]

    plt.figure()
    plt.plot(x, f, linewidth=2)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Densidade GLD–FKML")
    if ylim is not None:
        plt.ylim(*ylim)
    plt.tight_layout()
    plt.show()


def plot_gld_vs_data(lambdas, n_points=2000, quantile_trim=1e-3, qp_min=1e-8, ylim=None):
    data = np.asarray(data, dtype=float)
    l1, l2, l3, l4 = lambdas

    # Curva da PDF GLD (robusta para evitar explosões numéricas)
    a = float(quantile_trim)
    u = np.linspace(a, 1.0 - a, n_points)
    x = gld_fkml_quantile(u, l1, l2, l3, l4)
    qp = gld_fkml_qprime(u, l2, l3, l4)

    mask = np.isfinite(x) & np.isfinite(qp) & (qp > qp_min)
    x, f = x[mask], (1.0 / qp[mask])

    order = np.argsort(x)
    x, f = x[order], f[order]

    return x, f


def glam_data_generator(lambdas, n_points=5000, quantile_trim=1e-3, qp_min=1e-8, ylim=None) -> list:
    l1, l2, l3, l4 = lambdas

    # Curva da PDF GLD (robusta para evitar explosões numéricas)
    a = float(quantile_trim)
    u = np.linspace(a, 1.0 - a, n_points)
    x = gld_fkml_quantile(u, l1, l2, l3, l4)
    qp = gld_fkml_qprime(u, l2, l3, l4)

    mask = np.isfinite(x) & np.isfinite(qp) & (qp > qp_min)
    x, f = x[mask], (1.0 / qp[mask])

    order = np.argsort(x)
    x, f = x[order], f[order]

    return list(x)


def state_limit_function(x: np.ndarray, n_latent_samples: int) -> tuple[np.ndarray, pd.DataFrame]:
    """State limit function with time effect. Considering Z_1 and Z_2 are the latent variables.
    
    :param x: Input variables [0] = Resistance R ; [1] = Load S
    :param n_latent_samples: Number of latent samples to be generated for each input sample
    
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
        df['g'] = df['r']/df['z1'] - df['s'] * df['z2']
        dfs.append(df)
        lambdas, _ = fit_gld_fkml_mle(df['g'].values)
        y_aux.append(lambdas)
        y = np.array(y_aux)
    return y, dfs


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


def state_limit_function_time_gumbel(x: np.ndarray, n_latent_samples: int, t: float = 0.0) -> tuple[np.ndarray, pd.DataFrame]:
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

            # 1. Cálculo do parâmetro de escala (beta)
            # beta = (Desvio Padrão * raiz(6)) / pi
            beta = (z2_sc * np.sqrt(6)) / np.pi

            # 2. Cálculo do parâmetro de localização (mu ou loc)
            # loc = Média - (beta * Constante de Euler)
            loc = z2_mu - (beta * np.euler_gamma)

            # 3. Geração da variável aleatória (usando gumbel_r para máximos)
            # Se fosse para mínimos, usaria gumbel_l
            z2aux.append(stats.gumbel_l.rvs(loc=loc, scale=beta, size=1)[0])
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


def co2_percentage_1900_1950(year):
    """CO2 atmosférico (%) para os períodos históricos 1900–1950
    """
    # crescimento médio ~0.30 ppm/year
    co2_ppm = 296.0 + 0.30 * (year - 1900)
    return co2_ppm / 1e4


def co2_percentage_1950_2000(year):
    """CO2 atmosférico (%) para os períodos históricos 1950–2000
    """
    # crescimento médio ~1.16 ppm/year
    co2_ppm = 311.0 + 1.16 * (year - 1950)
    return co2_ppm / 1e4


def co2_percentage_pos2000(year):
    """CO2 atmosférico (%) para os períodos históricos pós-2000
    """

    t = year - 2000

    C0 = 369.0   # ppm em 2000
    a  = 1.85    # ppm/year
    b  = 0.018   # ppm/year²

    co2_ppm = C0 + a * t + b * t**2
    return co2_ppm / 1e4


def co2_percentage_year(year):
    """Concentração média global de CO2 atmosférico (%) válida de 1900 em diante.
    """

    if year <= 1950:
        return co2_percentage_1900_1950(year)
    elif 1950 < year <= 2000:
        return co2_percentage_1950_2000(year)
    else:
        return co2_percentage_pos2000(year)


# Beam class
class Beam():
    def __init__(self, geo: dict, mat: dict, load: dict, expo: dict):  
        """Initializes a Beam object with geometric, material, load, and exposure properties.
        
        :param geo: Geometric properties of the beam
        :param mat: Material properties of the beam
        :param load: Load properties of the beam
        :param expo: Exposure conditions for carbonation
        """

        self.geo = geo
        self.mat = mat
        self.load = load
        self.expo = expo

    def latent_variable_generator(self, n_samples: int) -> tuple:
        """Generates latent variables related the beam problem.

        :param n_samples: Number of latent samples to generate.
        :return: Tuple containing arrays of sampled live load, temperature, and relative humidity.
        """

        # qk_mean     = self.load['q_k [kN/m]']
        temp_mean   = self.expo['Temperature [°C]']
        rh_mean     = self.expo['Relative humidity [%]']
        # cov_q       = 0.20
        cov_temp    = 0.20
        cov_rh      = 0.20

        # qk_beam   = np.random.normal(loc=qk_mean, scale=abs(qk_mean) * cov_q, size=n_samples)
        temp_beam = np.random.normal(loc=temp_mean, scale=abs(temp_mean) * cov_temp, size=n_samples)
        rh_beam   = np.random.normal(loc=rh_mean, scale=abs(rh_mean) * cov_rh, size=n_samples)

        return (temp_beam, rh_beam)

    def carbonation_depth_at_time(self, model: Any, times: list, co2_perc: float, rh: float) -> tuple[float, list]:
        """Computes the carbonation depth at time t using a trained ML model.

        :param model: Trained ML model for carbonation depth prediction
        :param times: Time points [in years] to evaluate
        :param co2_perc: CO2 concentration [%]
        :param rh: Relative humidity [%]

        :return: [0] Time to reach the cover depth [year], [1] Carbonation depths at specified times [mm]
        """

        depths = []
        for t in times:
            df = pd.DataFrame({
                                    't (years)': [t],
                                    'CO2 (%)': [co2_perc],
                                    'fc (MPa)': [self.mat['f_ck [kPa]'] / 1000],
                                    'RH (%)': [rh],
                                    'Type of cement': [self.mat['Type of cement']],
                                    'Exposure conditions': [self.expo['Exposure conditions']]
                                })
            df = df[model.feature_names_in_]
            depths.append(float(model.predict(df)[0]))

        time_to_cover = np.interp(self.geo['cover [mm]'], depths, times)

        return float(time_to_cover), depths

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


# State limit function with time effect
def state_limit_function_time(x: np.ndarray, carb_model: Any, time_step: float = 0.0, n_latent_samples: int = 5000) -> tuple[np.ndarray, list]:
    z1, z2, z3 = [], [], []
    dfs = []
    lambdas_dfs = []
    for i in range(x.shape[0]):
        # Create Beam instance
        geo = {
                'b_w [m]':     float(x[i][0]), 
                'h [m]':       float(x[i][1]), 
                'cover [m]':   float(x[i][2])
              }
        mat = {
                'f_ck [kPa]':  float(x[i][3]),
                'Type of cement': 3
              } 
        expo = {
                'Installation year':   1990,
                'Exposure conditions': 2,
               }
        load = {}           
        beam_instance = Beam(geo=geo, mat=mat, load=load, expo=expo)

        # Latent variables
        latent_data   = beam_instance.latent_variable_generator(n_samples=n_latent_samples)
        temp_beam = latent_data[0]    # Temperature - latent variable
        rh_beam   = latent_data[1]    # Relative Humidity - latent variable
        df = pd.DataFrame({})
        df['z1'] = temp_beam
        df['z2'] = rh_beam       
        # Resistance
        df['r'] = float(x[i][2])
        

        # Carbonation profile
        name_best_model = 'model_NeuralNetwork_MLP_fold_4.pkl'
        model = joblib.load(name_best_model)
        s = []
        for _, row in df.iterrows():
            # Carbonation profle
            # df = {'t (years)': list(range(0, 150))}
            # df = pd.DataFrame(df)
            # co2list = []
            # for t in df['t (years)']:
            #     if t == 0:
            #         co2_percentage = co2_percentage_year(1990)
            # df['CO2 (%)']  = CO2_ppm / 10000
            df['fc (MPa)']            = float(x[i][3]) / 1000
            df['RH (%)']              = rh_beam
            df['Type of cement']      = mat['Type of cement']
            df['Exposure conditions'] = expo['Exposure conditions'] 
            expected_order = list(model.feature_names_in_)
            df = df[expected_order]
            df_aux = df.copy()
            y_pred = model.predict(df)
            df_aux['carb. depth (mm)'] = list(y_pred)
            df_aux['carb. depth (mm)'] = df_aux['carb. depth (mm)'].cummax()
            s.append(df_aux[df['t (years)'] == time_step]['carb. depth (mm)'].values[0])

        # State limit function and GLAM fitting
        df['s'] = s
        df['g'] = df['r'] - df['s']
        lambdas, _ = fit_gld_fkml_mle(df['g'].values)
        lambdas_dfs.append(lambdas)
        dfs.append(df)

    return np.array(lambdas_dfs), dfs



# State limit function with time effect
def state_limit_function_time(x: np.ndarray, carb_model: Any, time_step: float = 0.0, n_latent_samples: int = 5000) -> tuple[np.ndarray, list]:
    z1, z2, z3 = [], [], []
    dfs = []
    lambdas_dfs = []
    for i in range(x.shape[0]):
        # Create Beam instance
        geo = {
                'b_w [m]':     float(x[i][0]), 
                'h [m]':       float(x[i][1]), 
                'cover [m]':   5.0
              }
        
        mat = {
                'f_ck [kPa]': 30000.0,}
        
        
        beam_instance = Beam(geo=geo, mat=mat[i], load=load[i], expo=expo[i])
        gk_beam       = load[i]['g_k [kN/m]']                                                                              # Permanent load - deterministic

        # Latent variables
        latent_data   = beam_instance.latent_variable_generator(n_samples=n_latent_samples)
        qk_beam   = latent_data[0]    # Live load - latent variable
        temp_beam = latent_data[1]    # Temperature - latent variable
        rh_beam   = latent_data[2]    # Relative Humidity - latent variable
        df = pd.DataFrame({})
        df['z1'] = qk_beam
        df['z2'] = temp_beam
        df['z3'] = rh_beam
        df['s'] = df.apply(lambda row: beam_instance.design_bending_moment(g_k=gk_beam, q_k=float(row['z1'])), axis=1)
        
        # Carbonation time
        times = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 125, 150, 180]
        co2 = co2_percentage_year(2000)
        df['time for carbonation to start [year]'] = df.apply(lambda row: beam_instance.carbonation_depth_at_time(model=carb_model, times=times, co2_perc=co2, rh=float(row['z3'])), axis=1)
        
        # Load and resistant moment
        for _, row in df.iterrows():
            t_carb = row['time for carbonation to start [year]']
            if time_step <= t_carb:
                a_st0 = beam_instance.geo['n bars'] * (np.pi * (beam_instance.geo['phi [m]'] / 1000)**2 / 4)
                df['r'] = df.apply(lambda row: beam_instance.design_resistant_bending_moment_without_corrosion(a_st=a_st0), axis=1)
            else:
                df['r'] = df.apply(lambda row: beam_instance.design_resistant_bending_moment_with_corrosion(t=time_step, t_carb=t_carb, temp=float(row['z2'])), axis=1)
        
        # State limit function and GLAM fitting
        df['g'] = df['r'] - df['s']
        lambdas, _ = fit_gld_fkml_mle(df['g'].values)
        lambdas_dfs.append(lambdas)
        dfs.append(df)

    return np.array(lambdas_dfs), dfs
