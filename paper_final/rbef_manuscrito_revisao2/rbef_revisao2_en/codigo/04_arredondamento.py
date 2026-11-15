# Kolmogorov-Smirnov distance between a sample and the model CDF
def dist_ks(sample, cdf):
    x = np.sort(sample)
    n = x.size
    F = cdf(x)
    i = np.arange(1, n + 1)
    return max(np.max(i / n - F), np.max(F - (i - 1) / n))

rng = np.random.default_rng(0)
step = 0.1                                       # recording step of the data (m/s)
Dn_cont, Dn_round = [], []
for _ in range(200):
    s = gld.rvs(size=v.size, random_state=rng)   # sample from the fitted GLD, taken as true
    r = np.round(s / step) * step                # rounding to 0.1 m/s
    Dn_cont.append(dist_ks(s, gld.cdf))
    Dn_round.append(dist_ks(r, gld.cdf))

print(np.median(Dn_cont))                        # without rounding
print(np.median(Dn_round), np.percentile(Dn_round, 95))   # with rounding
