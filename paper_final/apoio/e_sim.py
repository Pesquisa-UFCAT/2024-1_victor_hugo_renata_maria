
import numpy as np
from scipy.stats import norm
import e_common as ec
K = ec.COEF['k_co_2']
PAR = dict(T_SL=150, r=0.04, eps=0.0, lam_insp=0.005, lam_prev=0.08, lam_corr=0.32,
           fck_0=20.0, fck_arg=30.0, ur=0.70, c_nom=25.0, a0=2000, scen="SSP2-4.5", post2100="const",
           sig_y=2.5, sig_c=1.5, cov=0.15)

def ppm_path(par, shock=None):
    t = np.arange(0, par['T_SL'] + 1)
    p = ec.co2_ppm(par['a0'] + t, par['scen'], par['post2100'])
    if shock is not None:
        ts, d, dur = shock.get('ts', 0), shock.get('d', 0.0), shock.get('dur', np.inf)
        p = p + d * ((t >= ts) & (t < ts + dur))
    return p

def pi_tables(par, eps_list=(0.0, 5.0, 10.0), n=40000, seed=123, shock=None):
    """Tabelas populacionais P[g<=eps] (pré-reparo): orig[a], arg[s,a] (reparo no ano s)."""
    L = ec.latents(n, par['ur'], par['cov'], seed)
    T = par['T_SL']; t = np.arange(0, T + 1); ppm = ppm_path(par, shock)
    c = par['c_nom'] * L['w_c']; ur = np.clip(par['ur'] * L['w_ur'], 0, 1)
    out = {}
    def tab(fc, s):
        a = t[s:] - s
        y = ec.possan(fc[:, None], a[None, :], ur[:, None], (ppm[s:] / 1e4)[None, :])
        y = np.maximum.accumulate(y, axis=1)
        g = c[:, None] - y
        return {e: np.mean(g <= e, axis=0) for e in eps_list}
    o = tab(par['fck_0'] * L['w_fc'], 0)
    for e in eps_list:
        out[('orig', e)] = o[e]; out[('arg', e)] = np.full((T + 1, T + 1), np.nan)
    fa = par['fck_arg'] * L['w_arg']
    for s in range(T + 1):
        o = tab(fa, s)
        for e in eps_list:
            out[('arg', e)][s, :T + 1 - s] = o[e]
    return out

def simulate(pstar, dt, par, variant='modelo', tables=None, n=20000, seed=7, shock=None, suspend=None):
    """Simulação em nível de realização (verdade) com decisão:
       variant='modelo'   : decisão comum a toda a população a partir de pi do modelo nominal (tabelas)
       variant='condicao' : cada realização inspecionada, g medido com erro; repara se P[g<=eps|medida]>p*.
       Retorna contagens anuais (média por elemento) de inspeção, reparo preventivo e corretivo + Pf(t)."""
    rng = np.random.default_rng(seed)
    T = par['T_SL']; eps = par['eps']
    L = ec.latents(n, par['ur'], par['cov'], seed)
    c = par['c_nom'] * L['w_c']; ur = np.clip(par['ur'] * L['w_ur'], 0, 1)
    fc = par['fck_0'] * L['w_fc']
    s_m, ln_sig = np.sqrt(np.log(1 + par['cov']**2)), None
    mu_m = -0.5 * s_m**2
    ppm = ppm_path(par, shock)
    s = np.zeros(n, int); ymax = np.zeros(n); nrep = np.zeros(n, int)
    c_meas = c + rng.normal(0, par['sig_c'], n)           # pacômetro (erro fixo por elemento)
    sig_g = np.hypot(par['sig_y'], par['sig_c'])
    thr = eps - sig_g * norm.ppf(pstar)                    # g_med < thr  <=>  P[g<=eps|med] > p*
    pop_s, pop_m = 0, 0                                    # estado comum (variante modelo)
    n_insp = np.zeros(T + 1); n_prev = np.zeros(T + 1); n_corr = np.zeros(T + 1); pf = np.zeros(T + 1)
    pf_insp = []; pi_model_log = []
    for t in range(1, T + 1):
        a = t - s
        y = ec.possan(fc, a, ur, ppm[t] / 1e4)
        ymax = np.maximum(ymax, y); g = c - ymax
        pf[t] = np.mean(g <= 0)
        insp = (t % dt == 0) and not (suspend is not None and suspend[0] < t <= suspend[0] + suspend[1])
        if not insp: continue
        n_insp[t] = 1.0; pf_insp.append((t, pf[t]))
        if variant == 'modelo':
            tb = tables[('orig', eps)] if pop_m == 0 else tables[('arg', eps)][pop_s]
            pim = tb[t - pop_s]; pi_model_log.append((t, pim))
            rep = np.full(n, pim > pstar)
            if pim > pstar: pop_s, pop_m = t, 1
        else:
            gmed = c_meas - (ymax + rng.normal(0, par['sig_y'], n))
            rep = gmed < thr
        if rep.any():
            corr = rep & (g <= 0)
            n_corr[t] = corr.mean(); n_prev[t] = (rep & ~corr).mean()
            k = rep.sum()
            fc[rep] = par['fck_arg'] * rng.lognormal(mu_m, s_m, k)
            s[rep] = t; ymax[rep] = 0.0; nrep[rep] += 1
    return dict(n_insp=n_insp, n_prev=n_prev, n_corr=n_corr, pf=pf, pf_insp=np.array(pf_insp),
                nrep_mean=nrep.mean(), nrep_q=np.quantile(nrep, [0.05, 0.5, 0.95]), pi_model=np.array(pi_model_log))

def cost(res, r=0.04, lam_insp=0.005, lam_prev=0.08, lam_corr=0.32):
    t = np.arange(len(res['n_insp'])); d = (1 + r) ** (-t)
    return 1 + np.sum(d * (lam_insp * res['n_insp'] + lam_prev * res['n_prev'] + lam_corr * res['n_corr']))

def maxpf(res, where='todas'):
    if where == 'insp': return res['pf_insp'][:, 1].max() if len(res['pf_insp']) else 0.0
    return res['pf'].max()
