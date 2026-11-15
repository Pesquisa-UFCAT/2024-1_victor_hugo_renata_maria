import pandas as pd

df = pd.read_csv("estacao_A001_diario.csv")
v = df["vento_ms"].dropna().to_numpy()         # daily mean wind speeds (m/s)

# method of moments from 15 starting points
sol = GlamFKML().fit_lambdas(v, n_starts=15, seed=0)
gld = GlamFKML(*sol.x)                         # fitted model
l1, l2, l3, l4 = sol.x

# support limits, as in the support equation
a = l1 - 1 / (l2 * l3) if l3 > 0 else -np.inf
b = l1 + 1 / (l2 * l4) if l4 > 0 else np.inf
outside = np.sum((v < a) | (v > b))            # observations outside the support
