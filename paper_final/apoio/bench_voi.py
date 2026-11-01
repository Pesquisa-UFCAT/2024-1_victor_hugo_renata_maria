"""Exemplo de referência (benchmark) do paper final: valor da informação de uma inspeção
em viga de concreto armado sujeita à carbonatação (modelo de Possan, MC direto).

Caso-base do manuscrito: f_c = 25 MPa, UR = 55 %, c_nom = 25 mm, CP II F, ambiente externo
protegido, construção em 1980, SSP2-4.5, latentes lognormais (f_c, c) e normal truncada (UR), CoV 0,15.
"""
import sys, json, numpy as np, pandas as pd, scipy.stats as ss
sys.path.insert(0, "inputs")
import possan_standalone as ps

# ----------------------------------------------------------------------------- dados
CO2 = ps.load_co2("inputs/co2_concentrations_1900_2100.csv")
FC0, UR0, C0, A0 = 25.0, 0.55, 25.0, 1980
CEM, EXP = 3, 2
V = 0.15
SL = np.sqrt(np.log(1 + V**2)); ML = -0.5 * SL**2
TS = np.arange(1, 101)                                   # idades (anos)
CO2P = np.array([ps.co2_percent(CO2, A0 + t) for t in TS])

# custos (múltiplos do custo de construção C0) e decisão
LP, LC, LINSP, R, W = 0.08, 0.32, 0.005, 0.04, 10
D = 1 / (1 + R)
LDEP_MIN = (LC - D**W * LC) / sum(D**k for k in range(W))   # limite físico: esperar com peça despassivada deve custar mais
LDEP = 0.02
SY, SC = 2.5, 1.5                                          # erros de medida (mm)
AGES = list(range(5, 55, 5))

def wur(n, seed):
    return ss.truncnorm.rvs((0 - 1) / V, (1 / UR0 - 1) / V, loc=1, scale=V, size=n, random_state=seed)

def depth(wf, wu):
    wf = np.atleast_1d(wf); wu = np.atleast_1d(wu)
    Y = np.empty((wf.size, TS.size))
    for j, t in enumerate(TS):
        Y[:, j] = ps.carbonation_depth_possan_by_type(FC0 * wf, t, UR0 * wu, CO2P[j], CEM, EXP, 0.0)
    return np.maximum.accumulate(Y, axis=1)

# ----------------------------------------------------------------------------- amostra a priori
rng = np.random.default_rng(2026)
N = 200_000
WF = rng.lognormal(ML, SL, N); WU = wur(N, 1); WC = rng.lognormal(ML, SL, N)
Y = depth(WF, WU); C = C0 * WC; G = C[:, None] - Y

# comonotonicidade (justifica atualização por quantil)
como = {}
for t1, t2 in [(10, 50), (20, 50), (20, 100), (30, 60)]:
    como[f"y_{t1}_{t2}"] = float(ss.spearmanr(Y[:50000, t1 - 1], Y[:50000, t2 - 1]).correlation)
    como[f"g_{t1}_{t2}"] = float(ss.spearmanr(G[:50000, t1 - 1], G[:50000, t2 - 1]).correlation)

# ----------------------------------------------------------------------------- representação por quantis (o que o emulador entrega)
NU, NCV = 2000, 400
U = (np.arange(NU) + 0.5) / NU
QY = np.quantile(Y, U, axis=0)                           # QY[u, t]: trajetória de profundidade do quantil u
VC = (np.arange(NCV) + 0.5) / NCV
CG = C0 * np.exp(ML + SL * ss.norm.ppf(VC))              # grade de cobrimento com massa a priori igual

def g_grid(tidx):                                        # g[u, c] na idade TS[tidx]
    return CG[None, :] - QY[:, tidx][:, None]

def action_costs(tm, lc=LC, ldep=LDEP):
    i = tm - 1
    g0 = g_grid(i)
    cR = np.where(g0 > 0, LP, lc)
    cE = D**W * np.where(g_grid(i + W) > 0, LP, lc)
    for k in range(W):
        cE = cE + ldep * D**k * (g_grid(i + k) <= 0)
    return cR, cE

def post_weights_u(yobs, tm, sy=SY):
    w = np.exp(-0.5 * ((yobs[:, None] - QY[None, :, tm - 1]) / sy) ** 2)
    return w / w.sum(1, keepdims=True)

def post_weights_c(cobs, sc=SC):
    w = np.exp(-0.5 * ((cobs[:, None] - CG[None, :]) / sc) ** 2)
    return w / w.sum(1, keepdims=True)

def voi_grid(tm, m=20000, seed=7, lc=LC, ldep=LDEP, sy=SY, sc=SC):
    r_ = np.random.default_rng(seed)
    iu = r_.integers(0, NU, m); ic = r_.integers(0, NCV, m)
    yobs = QY[iu, tm - 1] + r_.normal(0, sy, m); cobs = CG[ic] + r_.normal(0, sc, m)
    cR, cE = action_costs(tm, lc, ldep)
    tR, tE = cR[iu, ic], cE[iu, ic]
    prior_R = cR.mean() < cE.mean()
    base = (tR if prior_R else tE).mean()
    out = {"idade": tm, "acao_sem_inspecao": "reparar" if prior_R else "esperar",
           "Pf_priori": float((g_grid(tm - 1) <= 0).mean())}
    Wu = post_weights_u(yobs, tm, sy)
    eR = (Wu @ cR).mean(1); eE = (Wu @ cE).mean(1)
    out["VoI_profundidade"] = float(base - np.where(eR < eE, tR, tE).mean())
    Wc = post_weights_c(cobs, sc)
    eR = ((Wu @ cR) * Wc).sum(1); eE = ((Wu @ cE) * Wc).sum(1)
    out["VoI_prof_cobrimento"] = float(base - np.where(eR < eE, tR, tE).mean())
    out["VoI_perfeita"] = float(base - np.minimum(tR, tE).mean())
    return out

# ----------------------------------------------------------------------------- verificação por amostragem por importância nas latentes
def voi_is(tm, m=3000, seed=11):
    r_ = np.random.default_rng(seed)
    wf = r_.lognormal(ML, SL, m); wc = r_.lognormal(ML, SL, m); wu = wur(m, seed + 1)
    yt = depth(wf, wu); ct = C0 * wc; gt = ct[:, None] - yt
    yo = yt[:, tm - 1] + r_.normal(0, SY, m); co = ct + r_.normal(0, SC, m)
    sub = slice(0, 100_000)
    Gs, Ys, Cs = G[sub], Y[sub], C[sub]
    def costs(GG):
        i = tm - 1
        cR = np.where(GG[:, i] > 0, LP, LC)
        cE = D**W * np.where(GG[:, i + W] > 0, LP, LC) + LDEP * sum(D**k * (GG[:, i + k] <= 0) for k in range(W))
        return cR, cE
    cR, cE = costs(Gs); tR, tE = costs(gt)
    prior_R = cR.mean() < cE.mean(); base = (tR if prior_R else tE).mean()
    res = {}
    for lab, usec in [("profundidade", False), ("prof_cobrimento", True)]:
        ch = np.empty(m)
        for s in range(0, m, 250):
            q = slice(s, s + 250)
            Wt = np.exp(-0.5 * ((yo[q][:, None] - Ys[None, :, tm - 1]) / SY) ** 2)
            if usec:
                Wt *= np.exp(-0.5 * ((co[q][:, None] - Cs[None, :]) / SC) ** 2)
            Wt /= Wt.sum(1, keepdims=True)
            ch[q] = np.where(Wt @ cR < Wt @ cE, tR[q], tE[q])
        res[lab] = float(base - ch.mean())
    return res

# ----------------------------------------------------------------------------- três vigas gêmeas
BEAMS = {"A": (1.15, 1.0, 1.10), "B": (1.0, 1.0, 1.0), "C": (0.85, 1.0, 0.85)}
beam_rows, post_curves = [], {"t": TS.tolist(), "priori": (G <= 0).mean(0).tolist()}
for k, (wf, wu, wc) in BEAMS.items():
    yk = depth(wf, wu)[0]; ck = C0 * wc; gk = ck - yk
    T = TS[np.argmax(gk <= 0)] if (gk <= 0).any() else np.inf
    yobs = np.array([yk[19]]); cobs = np.array([ck])
    wu_ = post_weights_u(yobs, 20)[0]; wc_ = post_weights_c(cobs)[0]
    pf_d = np.array([(wu_[:, None] * (g_grid(j) <= 0)).sum(0).mean() for j in range(TS.size)])
    pf_dc = np.array([wu_ @ (g_grid(j) <= 0) @ wc_ for j in range(TS.size)])
    wis = np.exp(-0.5 * ((yobs[0] - Y[:, 19]) / SY) ** 2); wis2 = wis * np.exp(-0.5 * ((cobs[0] - C) / SC) ** 2)
    pf_is_d = (wis[:, None] * (G <= 0)).sum(0) / wis.sum(); pf_is_dc = (wis2[:, None] * (G <= 0)).sum(0) / wis2.sum()
    post_curves[f"{k}_prof"] = pf_d.tolist(); post_curves[f"{k}_prof_cob"] = pf_dc.tolist()
    post_curves[f"{k}_g"] = gk.tolist()
    cR, cE = action_costs(20)
    eR_d, eE_d = (wu_ @ cR).mean(), (wu_ @ cE).mean(); eR_dc, eE_dc = wu_ @ cR @ wc_, wu_ @ cE @ wc_
    beam_rows.append(dict(viga=k, fc_real=FC0 * wf, c_real=ck, y20=yk[19], g20=gk[19],
                          T_desp=float(T), Pf50_priori=float((G[:, 49] <= 0).mean()),
                          Pf50_prof=pf_d[49], Pf50_prof_cob=pf_dc[49],
                          dif_max_quantil_vs_IS_prof=float(np.abs(pf_d - pf_is_d).max()),
                          dif_max_quantil_vs_IS_prof_cob=float(np.abs(pf_dc - pf_is_dc).max()),
                          decisao_prof="reparar" if eR_d < eE_d else "esperar",
                          decisao_prof_cob="reparar" if eR_dc < eE_dc else "esperar"))
beams = pd.DataFrame(beam_rows)

# ----------------------------------------------------------------------------- regra de decisão aos 20 anos
cR, cE = action_costs(20)
ygrid = np.linspace(5, 35, 301)
Wy = post_weights_u(ygrid, 20)
dR = (Wy @ cR).mean(1) - (Wy @ cE).mean(1)
y_star = float(ygrid[np.argmax(dR < 0)])                 # acima disso, reparar (só profundidade)
cgrid = np.linspace(15, 35, 201)
Wcg = post_weights_c(cgrid)
diff_map = (Wy @ cR) @ Wcg.T - (Wy @ cE) @ Wcg.T         # [y, c]: <0 → reparar

# ----------------------------------------------------------------------------- VoI × idade, convergência, verificação, sensibilidade
voi = pd.DataFrame([voi_grid(t) for t in AGES])
conv = pd.DataFrame([dict(m=m, semente=s, **{k: v for k, v in voi_grid(20, m=m, seed=s).items() if k.startswith("VoI")})
                     for m in (1000, 5000, 20000) for s in (1, 2, 3)])
ver = []
for tm in (20, 30):
    a = voi_grid(tm); b = voi_is(tm)
    ver.append(dict(idade=tm, VoI_prof_quantil=a["VoI_profundidade"], VoI_prof_IS=b["profundidade"],
                    VoI_pc_quantil=a["VoI_prof_cobrimento"], VoI_pc_IS=b["prof_cobrimento"]))
ver = pd.DataFrame(ver)
sens = []
for ratio in (2, 4, 8):
    for ldep in (round(LDEP_MIN, 4), 0.02, 0.04):
        for sy in (1.5, 2.5, 4.0):
            df = pd.DataFrame([voi_grid(t, m=5000, lc=ratio * LP, ldep=ldep, sy=sy) for t in AGES])
            ib = df["VoI_prof_cobrimento"].idxmax()
            paga = df.loc[df["VoI_prof_cobrimento"] > LINSP, "idade"]
            sens.append(dict(razao_corr_prev=ratio, lambda_dep=ldep, sigma_y=sy,
                             idade_otima=int(df.loc[ib, "idade"]), VoI_max_pc=float(df.loc[ib, "VoI_prof_cobrimento"]),
                             VoI_max_prof=float(df["VoI_profundidade"].max()),
                             janela_paga=(f"{paga.min()}–{paga.max()}" if len(paga) else "nenhuma")))
sens = pd.DataFrame(sens)

np.savez_compressed("bench/bench_state.npz", QY=QY, CG=CG, U=U, ygrid=ygrid, cgrid=cgrid, diff_map=diff_map,
                    Gq=np.percentile(G, [5, 50, 95], axis=0))
beams.to_csv("bench/bench_vigas.csv", index=False)
voi.to_csv("bench/bench_voi_idade.csv", index=False)
conv.to_csv("bench/bench_convergencia.csv", index=False)
ver.to_csv("bench/bench_verificacao.csv", index=False)
sens.to_csv("bench/bench_sensibilidade.csv", index=False)
TT = np.where((G <= 0).any(1), TS[np.argmax(G <= 0, 1)], 999)
json.dump(dict(comonotonicidade=como, y_star_20=y_star, LDEP_MIN=LDEP_MIN, LDEP=LDEP,
               prior_T=dict(P05=float(np.percentile(TT, 5)), P50=float(np.percentile(TT, 50)),
                            P_T_100=float((G[:, -1] <= 0).mean())),
               post_curves=post_curves), open("bench/bench_resumo.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok")
