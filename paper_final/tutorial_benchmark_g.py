"""
Tutorial do benchmark do paper final — valor da informação de uma inspeção usando o emulador PyGLAM de g(t).

Rodar a partir da RAIZ do repositório, no .venv do projeto:
    python paper_final/tutorial_benchmark_g.py
Variáveis de ambiente opcionais:
    REPO_DIR  (padrão: pasta-mãe deste script)           pasta que contém functions.py e durability/
    OUT_DIR   (padrão "paper2_bench")  pasta de saída (CSVs e figuras)

Cada PASSO imprime os números que devem aparecer. O tutorial em Markdown explica cada passo.
"""
import os, sys, json
from pathlib import Path
import numpy as np, pandas as pd, dill

REPO = Path(os.environ.get("REPO_DIR", Path(__file__).resolve().parent.parent)).resolve()
OUT = Path(os.environ.get("OUT_DIR", "paper2_bench")); OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO))
from functions import (gld_quantile_at_u, generate_latent_variables,
                       carbonation_depth_possan_by_type, co2_percentage_year)

# =============================================================================
# PASSO 0 — Configuração do caso-base e das regras de custo
# =============================================================================
FCK, RH, COV = 25.0, 55.0, 25.0              # x = {f_c [MPa], UR [%], c_nom [mm]}
INSTALL, CEM, EXPO, CO2S = 1980, 3, 2, "SSP2-4.5"
LATENT_COV = 0.15
TS = np.arange(1, 101).astype(float)          # idades de 1 a 100 anos (passo anual)
NU = 2000                                     # nº de quantis da nuvem (trajetórias do emulador)
U = (np.arange(NU) + 0.5) / NU                # níveis de quantil u (mesma massa 1/NU cada)

LP, LC = 0.08, 0.32                           # reparo preventivo / corretivo (× C0)
LDEP = 0.02                                   # custo de risco por ano despassivado sem reparo (× C0)
LINSP = 0.005                                 # custo da inspeção (× C0)
TAXA, W = 0.04, 10                            # desconto real anual; espera de W anos
D = 1 / (1 + TAXA)
SIG_Y, SIG_C = 2.5, 1.5                       # erro da fenolftaleína e do pacômetro (mm) — HIPÓTESES
SIG_G = np.hypot(SIG_Y, SIG_C)                # erro da margem medida g_obs = c_obs − y_obs
AGES = list(range(5, 55, 5))

def ldep_min(lc=LC):
    """Limite físico: esperar com a peça despassivada tem de custar mais que reparar já."""
    return lc * (1 - D**W) / sum(D**k for k in range(W))

print(f"PASSO 0: sigma_g = {SIG_G:.2f} mm | d^10 = {D**W:.4f} | soma d^k (k=0..9) = {sum(D**k for k in range(W)):.3f}"
      f" | lambda_dep mínimo = {ldep_min():.4f} (usado {LDEP})")

# =============================================================================
# PASSO 1 — A nuvem do emulador: lambdas(t) pela NN e quantis da GLD
# =============================================================================
tag = f"install_{INSTALL}_cement_{CEM}_exposure_{EXPO}_co2_{CO2S}"
ddir = REPO / "durability"
m1 = dill.load(open(ddir / f"2500_nn_lambda_1_model_durability_{tag}.pkl", "rb"))
m2 = dill.load(open(ddir / f"2500_nn_lambda_2_model_durability_{tag}.pkl", "rb"))
sc = dill.load(open(ddir / f"2500_nn_scaler_durability_{tag}.pkl", "rb"))
dfnn = dill.load(open(ddir / f"2500_dataset_nn_durability_{tag}.pkl", "rb"))
lam_df = pd.DataFrame({"fck": FCK, "rh": RH, "cov": COV, "Time (years)": TS})
Xs = sc.transform(lam_df[["fck", "rh", "cov", "Time (years)"]].to_numpy())
lam_df["lambda 1"] = m1.predict(Xs); lam_df["lambda 2"] = m2.predict(Xs)
lam_df["lambda 3"] = float(dfnn["lambda 3"].mean()); lam_df["lambda 4"] = float(dfnn["lambda 4"].mean())
LAM = lam_df[["lambda 1", "lambda 2", "lambda 3", "lambda 4"]].to_numpy()
# QG[u, t] = Q_g(u; lambdas(t)). Linha = uma trajetória da nuvem (u fixo no tempo = acoplamento quantílico)
QG = np.array([gld_quantile_at_u(LAM[j], U) for j in range(TS.size)]).T
QG = np.minimum.accumulate(QG, axis=1)       # garante g não crescente (corrige ruído numérico)
print("PASSO 1: P[g<=0] do emulador aos 20/30/50/100 anos =",
      [round(float((QG[:, t - 1] <= 0).mean()), 4) for t in (20, 30, 50, 100)])

# =============================================================================
# PASSO 2 — Gabarito: o próprio simulador (Possan + latentes) em trajetórias
# =============================================================================
NSIM = 100_000
np.random.seed(2026)
rh_l, fck_l, cov_l = generate_latent_variables(NSIM, cov=LATENT_COV, rh_base=RH)
fck_e = np.clip(FCK * fck_l, 0, None); ur_e = np.clip(RH * rh_l, 0, 100) / 100; c_e = np.clip(COV * cov_l, 0, None)
YS = np.empty((NSIM, TS.size))
for j, t in enumerate(TS):
    YS[:, j] = carbonation_depth_possan_by_type(fck_e, t, ur_e, co2_percentage_year(INSTALL + t, CO2S), CEM, EXPO, 0.0)
YS = np.maximum.accumulate(YS, axis=1)
GS = c_e[:, None] - YS                          # trajetórias "verdadeiras" de g
QS = np.quantile(GS, U, axis=0)                 # a mesma nuvem em quantis, mas vinda do simulador
diag = pd.DataFrame([dict(idade=t,
                          Pf_simulador=float((GS[:, t - 1] <= 0).mean()),
                          Pf_emulador=float((QG[:, t - 1] <= 0).mean()),
                          g05_sim=np.percentile(GS[:, t - 1], 5), g05_emu=np.percentile(QG[:, t - 1], 5),
                          g50_sim=np.percentile(GS[:, t - 1], 50), g50_emu=np.percentile(QG[:, t - 1], 50))
                     for t in (10, 20, 25, 30, 50, 75, 100)])
diag.to_csv(OUT / "passo2_diagnostico_emulador.csv", index=False)
print("PASSO 2: diagnóstico emulador × simulador\n", diag.round(3).to_string(index=False))

# =============================================================================
# PASSO 3 — Custo de cada trajetória para as duas ações aos tm anos
# =============================================================================
def costs(Gp, tm, lc=LC, ldep=LDEP):
    """Gp[n, t]: trajetórias de g. Retorna (custo de reparar já, custo de esperar W anos) por trajetória."""
    i = tm - 1
    cR = np.where(Gp[:, i] > 0, LP, lc)
    cE = D**W * np.where(Gp[:, i + W] > 0, LP, lc) + ldep * sum(D**k * (Gp[:, i + k] <= 0) for k in range(W))
    return cR, cE

def categoria(Gp, tm):
    """0 = passiva até tm+W; 1 = despassiva durante a espera; 2 = já despassivada em tm."""
    i = tm - 1
    return np.where(Gp[:, i] <= 0, 2, np.where(Gp[:, i + W] <= 0, 1, 0))

# =============================================================================
# PASSO 4 — Uma viga: leitura → filtro da nuvem → custos esperados → decisão
# =============================================================================
def pesos(g_obs, Q, tm, sg=SIG_G):
    w = np.exp(-0.5 * ((np.atleast_1d(g_obs)[:, None] - Q[None, :, tm - 1]) / sg) ** 2)
    return w / w.sum(1, keepdims=True)

def explica_viga(nome, g_obs, Q, tm=20, w=None):
    cR, cE = costs(Q, tm); cat = categoria(Q, tm)
    w = np.full(Q.shape[0], 1 / Q.shape[0]) if w is None else w
    rows = []
    for k, lab in enumerate(["passiva até +10", "despassiva na espera", "já despassivada"]):
        mk = cat == k; p = w[mk].sum()
        rows.append(dict(viga=nome, categoria=lab, fracao=p,
                         custo_R=(w[mk] @ cR[mk]) / p if p > 0 else np.nan,
                         custo_E=(w[mk] @ cE[mk]) / p if p > 0 else np.nan))
    eR, eE = w @ cR, w @ cE
    rows.append(dict(viga=nome, categoria="MÉDIA PONDERADA", fracao=1.0, custo_R=eR, custo_E=eE))
    print(f"  {nome}: E[R] = {eR:.4f}, E[E] = {eE:.4f} -> {'REPARAR' if eR < eE else 'ESPERAR'}")
    return rows

print("PASSO 4: vigas didáticas aos 20 anos (emulador)")
ex = explica_viga("sem inspeção", None, QG)
for nome, gobs in [("leitura folgada g_obs=18 mm", 18.0), ("leitura média g_obs=10 mm", 10.0),
                   ("leitura crítica g_obs=2 mm", 2.0)]:
    ex += explica_viga(nome, gobs, QG, w=pesos(gobs, QG, 20)[0])
pd.DataFrame(ex).to_csv(OUT / "passo4_vigas_custos.csv", index=False)

# regra de decisão: abaixo de que g_obs vale reparar?
gg = np.linspace(-5, 30, 701); Wg = pesos(gg, QG, 20); cR, cE = costs(QG, 20)
g_star = float(gg[np.argmax((Wg @ cR) >= (Wg @ cE))])
print(f"  regra aos 20 anos: reparar se g_obs < {g_star:.1f} mm; esperar caso contrário")

# =============================================================================
# PASSO 5 — População de vigas virtuais (experimento gêmeo) e VoI
# =============================================================================
def voi(Qmodel, Gtrue, tm, sg=SIG_G, m=4000, seed=5, lc=LC, ldep=LDEP):
    """Decide com a nuvem Qmodel; cobra com as trajetórias verdadeiras Gtrue."""
    r = np.random.default_rng(seed)
    gt = Gtrue[r.integers(0, Gtrue.shape[0], m)]
    gobs = gt[:, tm - 1] + r.normal(0, sg, m)            # leituras sintéticas
    tR, tE = costs(gt, tm, lc, ldep)                     # custo verdadeiro de cada ação, por viga
    cR, cE = costs(Qmodel, tm, lc, ldep)                 # custo segundo o modelo, por trajetória da nuvem
    priori_R = cR.mean() < cE.mean()
    sem = (tR if priori_R else tE).mean()
    Wp = pesos(gobs, Qmodel, tm, sg)
    dec_R = (Wp @ cR) < (Wp @ cE)
    com = np.where(dec_R, tR, tE).mean()
    return dict(idade=tm, acao_sem_inspecao="reparar" if priori_R else "esperar",
                custo_sem=sem, custo_com=com, VoI=sem - com, VoI_perfeita=sem - np.minimum(tR, tE).mean(),
                frac_esperar=float((~dec_R).mean()), paga=bool(sem - com > LINSP))

r20 = voi(QG, QG, 20)
print(f"PASSO 5: aos 20 anos (emulador): sem inspeção {r20['custo_sem']:.4f}, com inspeção {r20['custo_com']:.4f}, "
      f"VoI {r20['VoI']:.4f} (custo do ensaio {LINSP}); {100 * r20['frac_esperar']:.1f}% das vigas liberadas para esperar")

# =============================================================================
# PASSO 6 — VoI × idade e validação pela decisão (emulador × simulador)
# =============================================================================
rows = []
for tm in AGES:
    a = voi(QG, QG, tm)              # mundo do emulador (o que o paper calcula)
    b = voi(QS, GS, tm)              # mundo do simulador (gabarito)
    c = voi(QG, GS, tm)              # decide com o emulador, cobra com o simulador
    rows.append(dict(idade=tm, acao_emulador=a["acao_sem_inspecao"], acao_simulador=b["acao_sem_inspecao"],
                     VoI_emulador=a["VoI"], VoI_simulador=b["VoI"], VoI_perfeita_sim=b["VoI_perfeita"],
                     custo_com_insp_simulador=b["custo_com"], custo_com_insp_decidindo_emulador=c["custo_com"],
                     arrependimento_com_insp=c["custo_com"] - b["custo_com"],
                     arrependimento_sem_insp=c["custo_sem"] - b["custo_sem"]))
voi_age = pd.DataFrame(rows); voi_age.to_csv(OUT / "passo6_voi_idade.csv", index=False)
print("PASSO 6:\n", voi_age.round(4).to_string(index=False))

# =============================================================================
# PASSO 7 — Sensibilidade (emulador): sigma_g, lambda_corr/lambda_prev, lambda_dep
# =============================================================================
sens = []
for ratio in (2, 4, 8):
    lc = ratio * LP
    for ldep in (0.02, 0.04):
        ok = ldep > ldep_min(lc)
        for sg in (1.5, SIG_G, 5.0):
            df = pd.DataFrame([voi(QG, QG, t, sg=sg, m=2000, lc=lc, ldep=ldep) for t in AGES])
            ib = df["VoI"].idxmax(); paga = df.loc[df["VoI"] > LINSP, "idade"]
            sens.append(dict(razao_corr_prev=ratio, lambda_dep=ldep, consistente=ok, sigma_g=round(sg, 2),
                             idade_otima=int(df.loc[ib, "idade"]), VoI_max=float(df.loc[ib, "VoI"]),
                             janela_paga=f"{paga.min()}–{paga.max()}" if len(paga) else "nenhuma"))
sens = pd.DataFrame(sens); sens.to_csv(OUT / "passo7_sensibilidade.csv", index=False)
print("PASSO 7:\n", sens.round(4).to_string(index=False))

# =============================================================================
# PASSO 8 — Figura de trabalho (nuvem + VoI × idade)
# =============================================================================
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for k in range(0, NU, 40):
    ax[0].plot(TS, QG[k], color="0.75", lw=0.5)
w1 = pesos(2.0, QG, 20)[0]; top = np.argsort(w1)[-60:]
for k in top:
    ax[0].plot(TS, QG[k], color="C3", lw=0.7, alpha=0.6)
ax[0].axhline(0, color="k", lw=0.8); ax[0].axvline(20, color="k", ls=":", lw=0.8)
ax[0].set(xlabel="Idade (anos)", ylabel="g(t) (mm)", title="Nuvem do emulador e filtro de g_obs = 2 mm")
ax[1].plot(gg, Wg @ cR, label="reparar já"); ax[1].plot(gg, Wg @ cE, label="esperar 10 anos")
ax[1].axvline(g_star, color="k", ls=":", lw=0.8)
ax[1].set(xlabel="g_obs aos 20 anos (mm)", ylabel="custo esperado (× C0)", title="Regra de decisão"); ax[1].legend()
ax[2].plot(voi_age.idade, voi_age.VoI_emulador, "o-", label="emulador")
ax[2].plot(voi_age.idade, voi_age.VoI_simulador, "s--", label="simulador (gabarito)")
ax[2].plot(voi_age.idade, voi_age.VoI_perfeita_sim, ":", color="0.4", label="informação perfeita")
ax[2].axhline(LINSP, color="C3", lw=0.8, label="custo do ensaio")
ax[2].set(xlabel="Idade da inspeção (anos)", ylabel="VoI (× C0)", title="Valor da inspeção"); ax[2].legend(fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "passo8_figura_trabalho.png", dpi=150)
json.dump(dict(g_star_20=g_star, VoI_20=r20, sigma_g=SIG_G, ldep_min=ldep_min()),
          open(OUT / "resumo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
print("FIM: arquivos em", OUT.resolve())
