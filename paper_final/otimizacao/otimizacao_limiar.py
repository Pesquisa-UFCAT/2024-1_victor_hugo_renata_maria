"""
Otimização da política de inspeção e reparo por limiar de margem g_lim — código-base.

Rodar a partir da RAIZ do repositório, no .venv do projeto:
    python paper_final/otimizacao/otimizacao_limiar.py

Se os .pkl treinados estiverem em durability/, usa o EMULADOR (NN -> lambdas -> GLD).
Se não estiverem, usa um SUBSTITUTO com a mesma interface: quantis empíricos do Possan
(simulador do functions.py), acoplados por quantil como no emulador. Troque depois.

Formulação completa e instruções: otimizacao_limiar.md (mesma pasta).
"""
import os, sys, itertools, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(os.environ.get("REPO_DIR", Path(__file__).resolve().parents[2])).resolve()
OUT = Path(os.environ.get("OUT_DIR", REPO / "paper2_otimizacao")); OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO))

T_VIDA = 100                       # horizonte (anos)
AGES = np.arange(0, T_VIDA + 1)    # idades 0..100 (anos inteiros)

# ============================================================================
# 1. A NUVEM: g(u, tau | x)  — trajetória de quantil u, idade tau, projeto x
# ============================================================================
class NuvemEmulador:
    """PyGLAM: NN prevê lambda1, lambda2 em cada idade; lambda3, lambda4 fixos (como no Paper 1)."""
    def __init__(self, x, repo=REPO, tag="install_1980_cement_3_exposure_2_co2_SSP2-4.5", n_lat=2500):
        import dill
        d = Path(repo) / "durability"
        m1 = dill.load(open(d / f"{n_lat}_nn_lambda_1_model_durability_{tag}.pkl", "rb"))
        m2 = dill.load(open(d / f"{n_lat}_nn_lambda_2_model_durability_{tag}.pkl", "rb"))
        sc = dill.load(open(d / f"{n_lat}_nn_scaler_durability_{tag}.pkl", "rb"))
        dfnn = dill.load(open(d / f"{n_lat}_dataset_nn_durability_{tag}.pkl", "rb"))
        fck, rh, cov = x
        X = sc.transform(np.c_[np.full(AGES.size, fck), np.full(AGES.size, rh), np.full(AGES.size, cov), AGES])
        self.l1, self.l2 = m1.predict(X), m2.predict(X)
        self.l3, self.l4 = float(dfnn["lambda 3"].mean()), float(dfnn["lambda 4"].mean())
        self.x = x

    def g(self, u, tau):
        tau = np.clip(np.asarray(tau, int), 0, T_VIDA)
        q = (u ** self.l3 - 1) / self.l3 - ((1 - u) ** self.l4 - 1) / self.l4
        return self.l1[tau] + q / self.l2[tau]


class NuvemSubstituta:
    """Substituto com a MESMA interface: quantis empíricos de g do simulador (Possan + latentes)."""
    def __init__(self, x, n=40_000, nu=2000, seed=2026, install=1980, cem=3, expo=2, co2s="SSP2-4.5", cov_lat=0.15):
        from functions import generate_latent_variables, carbonation_depth_possan_by_type, co2_percentage_year
        fck, rh, cov = x
        np.random.seed(seed)
        rl, fl, cl = generate_latent_variables(n, cov=cov_lat, rh_base=rh)
        fc_e = np.clip(fck * fl, 0, None); ur_e = np.clip(rh * rl, 0, 100) / 100; c_e = np.clip(cov * cl, 0, None)
        Y = np.zeros((n, AGES.size))
        for j, t in enumerate(AGES[1:], start=1):
            Y[:, j] = carbonation_depth_possan_by_type(fc_e, float(t), ur_e, co2_percentage_year(install + t, co2s), cem, expo, 0.0)
        G = c_e[:, None] - np.maximum.accumulate(Y, axis=1)
        self.U = (np.arange(nu) + 0.5) / nu
        self.Q = np.quantile(G, self.U, axis=0)            # Q[u, tau]
        self.x = x

    def g(self, u, tau):
        iu = np.clip((np.asarray(u) * self.Q.shape[0]).astype(int), 0, self.Q.shape[0] - 1)
        return self.Q[iu, np.clip(np.asarray(tau, int), 0, T_VIDA)]


def nuvem(x):
    try:
        return NuvemEmulador(x)
    except FileNotFoundError:
        print(f"  [aviso] .pkl do emulador não encontrados; usando NuvemSubstituta para x = {x}")
        return NuvemSubstituta(x)

# ============================================================================
# 2. SIMULADOR DA POLÍTICA theta = (t1, dt, g_lim, fc_rep) ao longo de 100 anos
# ============================================================================
CUSTOS = dict(insp=0.005, prev=0.08, corr=0.32, dep=0.02, taxa=0.04)   # × C0 (ILUSTRATIVOS)
SIG_G = float(np.hypot(2.5, 1.5))                                     # erro da margem medida (mm)

def simular(theta, x, nuvens, M=20_000, seed=1, custos=CUSTOS, sig_g=SIG_G):
    """Monte Carlo de M vigas sob a política theta. Mesma semente = números aleatórios comuns entre políticas."""
    t1, dt, glim, fc_rep = theta
    nv0 = nuvens[("orig", x)]
    nvr = nuvens[("rep", (fc_rep, x[1], x[2]))]
    r = np.random.default_rng(seed)
    u = r.random(M)                       # quantil da viga original (fixo no tempo)
    u_rep = r.random((M, 20))             # quantis dos materiais de reparo (um por reparo)
    eps = r.normal(0, sig_g, (M, T_VIDA + 1))
    d = 1 / (1 + custos["taxa"])
    t_rep = np.zeros(M, int); k_rep = np.zeros(M, int); n_prev = np.zeros(M); n_corr = np.zeros(M)
    anos_dep = np.zeros(M); ever = np.zeros(M, bool); custo = np.zeros(M); gmin = np.full(M, np.inf)
    insp = set(range(t1, T_VIDA, dt))
    pf_inst = np.zeros(T_VIDA + 1)
    for t in range(1, T_VIDA + 1):
        tau = t - t_rep
        g = np.where(k_rep == 0, nv0.g(u, tau), nvr.g(u_rep[np.arange(M), np.minimum(k_rep - 1, 19)], tau))
        gmin = np.minimum(gmin, g); g = gmin   # g não cresce dentro de um ciclo
        dep = g <= 0
        pf_inst[t] = dep.mean(); anos_dep += dep; ever |= dep; custo += custos["dep"] * d**t * dep
        if t in insp:
            custo += custos["insp"] * d**t
            rep = (g + eps[:, t]) <= glim
            corr, prev = rep & dep, rep & ~dep
            n_prev += prev; n_corr += corr
            custo += d**t * (custos["prev"] * prev + custos["corr"] * corr)
            t_rep[rep] = t; k_rep[rep] += 1; gmin[rep] = np.inf
    N = n_prev + n_corr
    return dict(t1=t1, dt=dt, g_lim=glim, fc_rep=fc_rep, N_insp=len(insp),
                E_Nrep=N.mean(), E_Ncorr=n_corr.mean(), P_N2=(N >= 2).mean(),
                P_desp=ever.mean(), EP_P_desp=np.sqrt(ever.mean() * (1 - ever.mean()) / M),
                Pf_inst_max=pf_inst.max(), E_anos_desp=anos_dep.mean(), custo=custo.mean())

# ============================================================================
# 3. OTIMIZAÇÃO: grade (etapa 1), restrição de confiabilidade, Pareto
# ============================================================================
def pareto(df, objs):
    """Linhas não dominadas (minimizar todas as colunas em objs)."""
    v = df[objs].to_numpy(); keep = np.ones(len(v), bool)
    for i in range(len(v)):
        if keep[i]:
            dom = np.all(v <= v[i], 1) & np.any(v < v[i], 1)
            if dom.any(): keep[i] = False
    return df[keep].sort_values(objs[0])

if __name__ == "__main__":
    from scipy.stats import norm
    X = (25.0, 55.0, 25.0)                       # f_c [MPa], UR [%], c_nom [mm]
    BETA = 1.3; P_ALVO = norm.cdf(-BETA)
    GRADE = dict(t1=[10, 15, 20], dt=[5, 10, 15, 20], g_lim=[0, 2, 4, 6, 8, 10, 12], fc_rep=[30.0, 40.0, 50.0])
    nuvens = {("orig", X): nuvem(X)}
    for fr in GRADE["fc_rep"]:
        nuvens[("rep", (fr, X[1], X[2]))] = nuvem((fr, X[1], X[2]))
    rows = [simular(th, X, nuvens) for th in itertools.product(*GRADE.values())]
    df = pd.DataFrame(rows); df.to_csv(OUT / "grade_politicas.csv", index=False)
    ok = df[df.P_desp <= P_ALVO]
    f1 = ok.sort_values(["E_Nrep", "N_insp"]).head(5)
    f2 = ok.sort_values("custo").head(5)
    par = pareto(ok, ["E_Nrep", "N_insp", "P_desp"])
    par.to_csv(OUT / "pareto_N_insp_risco.csv", index=False)
    cols = ["t1", "dt", "g_lim", "fc_rep", "N_insp", "E_Nrep", "P_N2", "P_desp", "custo"]
    print(f"P_alvo = {P_ALVO:.4f} | {len(df)} políticas, {len(ok)} viáveis")
    print("F1 — menos reparos (desempate: menos inspeções):\n", f1[cols].round(4).to_string(index=False))
    print("F2 — menor custo:\n", f2[cols].round(4).to_string(index=False))
    print(f"F3 — Pareto (reparos, inspeções, risco): {len(par)} políticas em pareto_N_insp_risco.csv")
    json.dump(dict(P_alvo=P_ALVO, n_politicas=len(df), n_viaveis=len(ok)), open(OUT / "resumo.json", "w"))
