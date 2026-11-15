# distância de Kolmogorov-Smirnov entre uma amostra e a acumulada do modelo
def dist_ks(amostra, cdf):
    x = np.sort(amostra)
    n = x.size
    F = cdf(x)
    i = np.arange(1, n + 1)
    return max(np.max(i / n - F), np.max(F - (i - 1) / n))

rng = np.random.default_rng(0)
passo = 0.1                                      # passo de registro dos dados (m/s)
Dn_cont, Dn_arr = [], []
for _ in range(200):
    s = gld.rvs(size=v.size, random_state=rng)   # amostra da GLD ajustada, tomada como verdadeira
    r = np.round(s / passo) * passo              # arredondamento a 0,1 m/s
    Dn_cont.append(dist_ks(s, gld.cdf))
    Dn_arr.append(dist_ks(r, gld.cdf))

print(np.median(Dn_cont))                        # sem arredondamento
print(np.median(Dn_arr), np.percentile(Dn_arr, 95))   # com arredondamento
