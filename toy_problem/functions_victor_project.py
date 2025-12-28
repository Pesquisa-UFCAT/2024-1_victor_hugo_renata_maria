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


def state_limit_function_time(x: np.ndarray, n_latent_samples: int, t: float = 0) -> tuple[np.ndarray, pd.DataFrame]:
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


def g_toy_problem_parallel_with_multiprocessing(x_val_list: np.ndarray | list, n_latent_samples: int, t: int = 0, n_processes: Optional[int] = None):
    if n_processes is None:
        n_processes = cpu_count()
    args_list = [(x_val_list[i], n_latent_samples, t) for i in range(len(x_val_list))]
    with Pool(processes=n_processes) as pool:
        results = pool.starmap(state_limit_function_time, args_list)
    y_list = [r[0] for r in results]
    df_list = [r[1] for r in results]
    # df = []
    # for sublist in y:

    return y_list, df_list
