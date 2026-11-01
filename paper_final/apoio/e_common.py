
import numpy as np, pandas as pd, importlib.util
from scipy import stats
_P = str(__import__("pathlib").Path(__file__).resolve().parent / "inputs" / "possan_standalone.py")
_C = str(__import__("pathlib").Path(__file__).resolve().parent / "inputs" / "co2_concentrations_1900_2100.csv")
spec = importlib.util.spec_from_file_location("possan_standalone", _P); ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
CO2DF = ps.load_co2(_C)
COEF = ps.possan_coefficients(3, 2)

def co2_ppm(year, scen="SSP2-4.5", post2100="const"):
    """ppm por ano-calendário; após 2100: 'const' (valor de 2100) ou 'lin' (tendência 2090-2100)."""
    year = np.asarray(year, float)
    yr = CO2DF["year"].values; v = CO2DF[scen].values
    out = np.interp(np.minimum(year, 2100.0), yr, v)
    if post2100 == "lin":
        slope = (v[yr == 2100][0] - v[yr == 2090][0]) / 10.0
        out = np.where(year > 2100, v[yr == 2100][0] + slope * (year - 2100), out)
    return out

def possan(fc, t, ur, co2pct):
    return ps.carbonation_depth_possan(f_ck=fc, t=t, ur=ur, co_2=co2pct, ad=0.0,
        k_c=COEF['k_c'], k_fc=COEF['k_fc'], k_ad=COEF['k_ad'], k_co_2=COEF['k_co_2'], k_rh=COEF['k_rh'], k_ce=COEF['k_ce'])

def latents(n, ur_nom, cov=0.15, seed=0):
    rng = np.random.default_rng(seed)
    s = np.sqrt(np.log(1 + cov**2)); m = -0.5 * s**2
    w_fc = rng.lognormal(m, s, n); w_c = rng.lognormal(m, s, n)
    a, b = (0 - 1) / cov, (1 / ur_nom - 1) / cov
    w_ur = stats.truncnorm.rvs(a, b, loc=1, scale=cov, size=n, random_state=rng)
    w_arg = rng.lognormal(m, s, n)   # latente da argamassa (1o reparo); reparos seguintes usam permutações
    return dict(w_fc=w_fc, w_c=w_c, w_ur=w_ur, w_arg=w_arg)

def first_cross(t, g, glim):
    """Tempo da 1a travessia g<=glim (interp. linear), np.inf se não cruza. g: (n, nt) não-crescente."""
    below = g <= glim
    idx = np.argmax(below, axis=1); ok = below.any(axis=1)
    T = np.full(g.shape[0], np.inf)
    i = idx[ok]; rows = np.where(ok)[0]
    i0 = np.maximum(i - 1, 0)
    g0, g1 = g[rows, i0], g[rows, i]
    frac = np.where((i > 0) & (g0 != g1), (g0 - glim) / (g0 - g1), 0.0)
    T[rows] = t[i0] + frac * (t[i] - t[i0])
    T[rows[i == 0]] = t[0]
    return T
