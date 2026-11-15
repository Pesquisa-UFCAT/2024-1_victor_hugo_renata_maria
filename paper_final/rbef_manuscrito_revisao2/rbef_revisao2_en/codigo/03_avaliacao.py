# quantile deviations, in m/s
p = np.array([0.05, 0.50, 0.95])
delta = gld.ppf(p) - np.quantile(v, p)

# Kolmogorov-Smirnov distance between the empirical CDF and the model CDF
x = np.sort(v)
n = x.size
F = gld.cdf(x)
i = np.arange(1, n + 1)
Dn = max(np.max(i / n - F), np.max(F - (i - 1) / n))
