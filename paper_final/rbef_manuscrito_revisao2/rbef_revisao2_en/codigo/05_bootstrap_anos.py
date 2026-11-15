# one array of temperatures for each July (each year is a block)
df["data"] = pd.to_datetime(df["data"])
july = df[(df["data"].dt.month == 7) & df["temperatura_c"].notna()]
years = [g["temperatura_c"].to_numpy() for _, g in july.groupby(july["data"].dt.year)]

rng = np.random.default_rng(0)
p = [0.05, 0.50, 0.95]
Q = []
for _ in range(1000):
    draw = rng.integers(0, len(years), len(years))        # years drawn with replacement
    sample = np.concatenate([years[i] for i in draw])     # joins the drawn Julys
    Q.append(np.quantile(sample, p))

print(np.std(Q, axis=0))     # standard deviation of the empirical quantiles across resamples
