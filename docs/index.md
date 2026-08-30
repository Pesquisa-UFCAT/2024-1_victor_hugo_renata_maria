# Carbonation Durability Surrogates

Reference documentation for `functions.py`, the module behind the carbonation
durability study: a CO{sub}`2` concentration model, a machine-learning carbonation
profile, a Generalized Lambda Distribution (GLD) emulator, and Polynomial Chaos
Expansion (PCE) surrogates fitted to the GLD lambdas at each time step.

## The pipeline in one line

```text
design samples  ->  emulator (latent sampling + GLD fit)  ->  lambda dataset  ->  PCE surrogate
```

Two parallel tracks share this structure:

`*_durability`
: The real problem. Carbonation depth of a reinforced concrete section, driven by
  `carb_model.predict` through {func}`functions.emulator_function_time_durability`.

`*_benchmark`
: The analytical R/S twin, $g = k(t) \cdot R / z_1 - S \cdot z_2$, used to validate
  the method against a known answer.

Each track can be run in one shot (`train_and_validate_pce_at_time*`) or split into
the expensive data generation stage and a cheap, repeatable PCE fit
(`generate_dataset_at_time_*` followed by `train_and_validate_pce_from_dataset_*`).

```{toctree}
:maxdepth: 2
:caption: Contents

usage
api
```

## Indices

- {ref}`genindex`
- {ref}`search`
