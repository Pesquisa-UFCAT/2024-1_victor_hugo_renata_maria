import os
from pathlib import Path

import numpy as np
import pandas as pd
from typing import Optional
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


# def bending_moment_simple_support_beam(q, l):
#     return p_gk * a_s * (l - a_s/2) / d

# def state_limit_function_time_real_beam(x: np.ndarray, n_latent_samples: int, cob, cement, expo, ratio_l_d, co2, t: float = 0.0) -> tuple[np.ndarray, pd.DataFrame]:
#     """State limit function with time effect. Evaluate state limit function for simple support reinforced concrete beam. 
    
#     :param x: Input variables [0] = Resistance R ; [1] = Load S
#     :param n_latent_samples: Number of latent samples to be generated for each input sample
#     :param t: Time parameter affecting the state limit function
    
#     :return: [0] = GLAM parameters ; [1] = Dataset with Resitance 'r', Load 's', latent variables 'z1' and 'z2', and state limit function 'g'
#     """
    
#     y_aux = []
#     dfs = []
#     for i in range(x.shape[0]):
#         # df = {'r': [x[i, 0]] * n_latent_samples, 's': [x[i, 1]] * n_latent_samples, 'cement': [cement] * n_latent_samples, 'expo': [expo] * n_latent_samples}
#         df = pd.DataFrame(df)
#         z1aux = []
#         z2aux = []
#         for i in df.iterrows():
#             z1_mu = 1.
#             z1_sc = 0.028
#             s = np.sqrt(np.log(1 + (z1_sc/z1_mu)**2))
#             scale = z1_mu / np.sqrt(1 + (z1_sc/z1_mu)**2)
#             z1aux.append(stats.norm.rvs(s=s, scale=scale, size=1)[0]) # umidade
#             p_qk = ratio_l_d * x[i, 0]
#             z2_mu = p_qk
#             z2_sc = z2_mu * 0.096
#             # Converter para gumbel certinho
#             z2aux.append(stats.gumbel_r.rvs(s=s, scale=scale, size=1)[0]) # carga (gumbel)
#         df['z1'] = z1aux
#         df['z2'] = z2aux
#         m_gk = bending_moment_simple_support_beam()
#         m_qk = bending_moment_simple_support_beam()
#         m_sd = 1.0 * m_gk + 1.0 * m_qk
#         total_time = list(range(0, 101))
#         y_depth = carbonation_depth(fck, cement, expo, total_time)
#         for j in range(len(total_time)):
#             if y_depth[j] >= cob:
#                 m_rd = 
#             else:
#                 m_rd = 
#         df['g'] = m_rd - m_sd
#         dfs.append(df)
#         lambdas, _ = fit_gld_fkml_mle(df['g'].values)
#         y_aux.append(lambdas)
#         y = np.array(y_aux)
    
#     return y, dfs


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


def nearest_time_in_dataset(bds, t_query):
    """
    Retorna o tempo disponível no dataset mais próximo de t_query.
    """
    time_available = np.sort(bds["time"].unique())
    idx = np.argmin(np.abs(time_available - t_query))
    return float(time_available[idx])


def resistant_moment_limit_single_reinforcement(
    b_w: float,
    h: float,
    f_ck: float,
    gamma_c: float = 1.4
) -> float:
    """
    Computes the resistant bending moment limit for a rectangular reinforced
    concrete beam section with single reinforcement according to NBR 6118.

    :param b_w: Beam width (m)
    :param h: Beam total height (m)
    :param f_ck: Characteristic concrete compressive strength (kPa)
    :param gamma_c: Partial safety factor for concrete

    :return: Resistant moment limit (N.m)
    """

    f_ck /= 1e3
    if f_ck > 50:
        lambda_c = 0.80 - (f_ck - 50) / 400
        alpha_c = (1.0 - (f_ck - 50) / 200) * 0.85
        beta = 0.35
    else:
        lambda_c = 0.80
        alpha_c = 0.85
        beta = 0.45

    f_ck *= 1e3
    f_cd = f_ck / gamma_c
    d = 0.9 * h

    return b_w * d**2 * lambda_c * beta * alpha_c * f_cd * (1 - 0.5 * lambda_c * beta)


def steel_area_single_reinforcement(
    m_sd: float,
    b_w: float,
    h: float,
    f_ck: float,
    f_ywk: float = 500000,
    gamma_c: float = 1.4,
    gamma_s: float = 1.15
) -> tuple[float, float]:
    """
    Computes the required steel reinforcement area for bending according to NBR 6118.

    :param m_sd: Design bending moment (N.m)
    :param b_w: Beam width (m)
    :param h: Beam total height (m)
    :param f_ck: Concrete compressive strength (kPa)
    :param f_ywk: Characteristic steel yield strength (Pa)

    :return: Steel area a_s (m²), reinforcement ratio rho_s (%)
    """

    f_ck /= 1e3
    if f_ck > 50:
        lambda_c = 0.80 - (f_ck - 50) / 400
        alpha_c = (1.0 - (f_ck - 50) / 200) * 0.85
    else:
        lambda_c = 0.80
        alpha_c = 0.85

    f_ck *= 1e3
    f_cd = f_ck / gamma_c
    d = 0.9 * h

    zeta = m_sd / (b_w * alpha_c * f_cd)
    x = (d - np.sqrt(d**2 - 2 * zeta)) / lambda_c
    z = d - 0.5 * lambda_c * x

    f_yd = f_ywk / gamma_s
    a_s = m_sd / (z * f_yd)
    rho_s = a_s / (b_w * h) * 100

    return a_s, rho_s


def resistant_bending_moment(
    a_s: float,
    b_w: float,
    h: float,
    f_ck: float,
    f_yk: float = 500000,
    gamma_s: float = 1.15,
    gamma_c: float = 1.40
) -> float:
    """
    Computes the resistant bending moment of a reinforced concrete beam section.

    :param a_s: Steel reinforcement area (m²)
    :param b_w: Beam width (m)
    :param h: Beam total height (m)
    :param f_ck: Concrete compressive strength (kPa)

    :return: Resistant bending moment R (N.m)
    """

    f_ck /= 1e3
    if f_ck > 50:
        lambda_c = 0.80 - (f_ck - 50) / 400
        alpha_c = (1.0 - (f_ck - 50) / 200) * 0.85
    else:
        lambda_c = 0.80
        alpha_c = 0.85

    f_ck *= 1e3
    f_cd = f_ck / gamma_c
    d = 0.9 * h

    x = (a_s * f_yk) / (f_cd * b_w * alpha_c * lambda_c)
    m_rd = a_s * f_yk * (d - 0.5 * lambda_c * x)

    return m_rd


def compute_RS_real_beam(
    b_w: float,
    h: float,
    f_ck: float,
    a_s: float,
    chi: float = 0.30,
    gamma_g: float = 1.40,
    gamma_q: float = 1.40,
    gamma_f: float = 1.00
) -> tuple[float, float]:
    """
    Computes deterministic resistance (R) and solicitation (S)
    for a real reinforced concrete beam based on mechanical models.

    :param b_w: Beam width (m)
    :param h: Beam total height (m)
    :param f_ck: Concrete compressive strength (kPa)
    :param a_s: Steel reinforcement area (m²)
    :param chi: Load combination factor
    :param gamma_g: Permanent load factor
    :param gamma_q: Variable load factor
    :param gamma_f: Global safety factor

    :return:
        R: Resistant bending moment
        S: Design solicitation bending moment
    """

    # --- Resistant bending moment ---
    R = resistant_bending_moment(
        a_s=a_s,
        b_w=b_w,
        h=h,
        f_ck=f_ck
    )

    # --- Load decomposition ---
    den_g = gamma_g + gamma_q * chi / (1.0 - chi)
    den_q = gamma_g * (1.0 - chi) / chi + gamma_q

    m_gk = R / den_g
    m_qk = R / den_q

    # --- Design solicitation ---
    S = gamma_f * (m_gk + m_qk)

    return R, S


def generate_x_from_real_beam(
    b_w: float,
    h: float,
    f_ck: float,
    a_s: float,
    chi: float = 0.30
) -> np.ndarray:
    """
    Generates input array x = [[R, S]] for the GLAM pipeline
    from a real reinforced concrete beam.
    """

    R, S = compute_RS_real_beam(
        b_w=b_w,
        h=h,
        f_ck=f_ck,
        a_s=a_s,
        chi=chi
    )

    return np.array([[R, S]])



def state_limit_function_time_real_beam(
    x: np.ndarray,
    n_latent_samples: int,
    t: float = 0.0
) -> tuple[np.ndarray, list[pd.DataFrame]]:
    """
    State limit function with time effect for a real reinforced concrete beam.
    Considering Z_1 and Z_2 as latent variables.

    :param x: Input variables [0] = Resistance R ; [1] = Load S
    :param n_latent_samples: Number of latent samples per realization
    :param t: Time parameter (years)

    :return:
        [0] GLAM parameters (lambdas)
        [1] List of DataFrames with r, s, z1, z2 and g
    """

    y_aux = []
    dfs = []

    for i in range(x.shape[0]):

        df = pd.DataFrame({
            'r': [x[i, 0]] * n_latent_samples,
            's': [x[i, 1]] * n_latent_samples
        })

        z1, z2 = [], []

        for _ in range(n_latent_samples):

            # --- Latent variable Z1 (resistance uncertainty) ---
            mu, sc = 1.0, 0.028
            s_ln = np.sqrt(np.log(1 + (sc / mu) ** 2))
            scale_ln = mu / np.sqrt(1 + (sc / mu) ** 2)
            z1.append(stats.lognorm.rvs(s=s_ln, scale=scale_ln))

            # --- Latent variable Z2 (load uncertainty) ---
            mu, sc = 1.0, 0.096
            s_ln = np.sqrt(np.log(1 + (sc / mu) ** 2))
            scale_ln = mu / np.sqrt(1 + (sc / mu) ** 2)
            z2.append(stats.lognorm.rvs(s=s_ln, scale=scale_ln))

        df['z1'] = z1
        df['z2'] = z2

        # --- Time degradation factor (generic – can be replaced by carbonation) ---
        k_t = 1 + (0.3 - 1.0) * t / 100

        df['g'] = k_t * df['r'] / df['z1'] - df['s'] * df['z2']

        lambdas, _ = fit_gld_fkml_mle(df['g'].values)

        y_aux.append(lambdas)
        dfs.append(df)

    return np.array(y_aux), dfs


