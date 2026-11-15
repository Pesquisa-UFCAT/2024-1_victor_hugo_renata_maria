# um vetor de temperaturas para cada julho (cada ano é um bloco)
dados["data"] = pd.to_datetime(dados["data"])
julho = dados[(dados["data"].dt.month == 7) & dados["temperatura_c"].notna()]
anos = [g["temperatura_c"].to_numpy() for _, g in julho.groupby(julho["data"].dt.year)]

rng = np.random.default_rng(0)
p = [0.05, 0.50, 0.95]
Q = []
for _ in range(1000):
    sorteio = rng.integers(0, len(anos), len(anos))        # anos sorteados com reposição
    amostra = np.concatenate([anos[i] for i in sorteio])   # reúne os julhos sorteados
    Q.append(np.quantile(amostra, p))

print(np.std(Q, axis=0))     # desvio padrão dos quantis empíricos entre reamostras
