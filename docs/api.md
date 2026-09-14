# API reference

```{eval-rst}
.. module:: functions
```

Every object below lives in `functions.py` at the repository root.

Autodoc emits reStructuredText, which MyST cannot reparse as Markdown, so the
directives below sit inside `{eval-rst}` blocks. The prose around them, and the
docstrings themselves, need no such wrapper.

## Atmospheric CO{sub}`2` model

Annual global CO{sub}`2` concentration from the published CMIP6 historical series
(1900–2014) and SSP1-2.6, SSP2-4.5 or SSP5-8.5 (2015–2100), expressed as a
percentage (ppm / 10000). The default scenario is SSP2-4.5. Fractional years are
linearly interpolated; extrapolation is rejected. The versioned local table and
its provenance live in `data/co2/`. No network connection is needed.

```python
co2_percentage_year(2050, "SSP2-4.5")  # approximately 0.0506875 (%)
co2_percentage_year(2100, "SSP5-8.5")  # approximately 0.1135210 (%)
```

Pass `co2_scenario="SSP1-2.6"` (or another supported scenario) to the durability
generation, profile and training functions. Output filenames include the scenario;
datasets produced with the old polynomial must be regenerated before training.

```{eval-rst}
.. autofunction:: co2_percentage_year
```

## Carbonation profile

Wraps a trained ML carbonation model into a calendar-year depth profile, and queries
that profile at an arbitrary year.

```{eval-rst}
.. autofunction:: carbonation_profile
.. autofunction:: _interp_profile_at
```

## Latent variables

Random multipliers that turn each deterministic design point into a distribution, one
pair of generators per track.

```{eval-rst}
.. autofunction:: generate_latent_variables
.. autofunction:: generate_latent_variables_benchmark
```

## Emulators

The expensive stage: for each design point, sample the latent variables, evaluate the
underlying model, and fit a Generalized Lambda Distribution to the resulting response.
Both return `(df_full, df_unique)`, where `df_unique` carries the GLD lambdas and the
per-design-point `Processing time (s)`.

```{eval-rst}
.. autofunction:: emulator_function_time_durability
.. autofunction:: emulator_function_time_benchmark
```

## Split pipeline

The same work in two stages, so the emulator run can be reused across PCE refits.
Stage 1 writes the lambda datasets to disk; stage 2 reads them back, fits the PCE and
scores it, making no emulator calls.

### Stage 1 — dataset generation

```{eval-rst}
.. autofunction:: generate_dataset_at_time_durability
.. autofunction:: generate_dataset_at_time_benchmark
```

### Stage 2 — PCE fit and validation

```{eval-rst}
.. autofunction:: train_and_validate_pce_from_dataset_durability
.. autofunction:: train_and_validate_pce_from_dataset_benchmark
```
