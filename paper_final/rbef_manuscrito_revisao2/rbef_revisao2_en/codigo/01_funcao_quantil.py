import numpy as np
from pyglam import GlamFKML

# GLD-FKML with lambda = (0, 1, 0.14, 0.14), a shape close to the normal
model = GlamFKML(0.0, 1.0, 0.14, 0.14)

# quantiles read directly from the quantile function Q(u)
median, p95 = model.ppf([0.50, 0.95])

# sampling by inverse transform, X = Q(U)
sample = model.rvs(size=1000, random_state=42)
