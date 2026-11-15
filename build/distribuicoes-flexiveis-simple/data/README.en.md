# Data sheet — automatic station A001 (Brasília, Brazil)

Items marked **[TODO]** must be completed or confirmed by the authors.

| Item | Value |
|---|---|
| Source | INMET Meteorological Database (BDMEP), https://bdmep.inmet.gov.br/ |
| Product / query | Daily automatic-station data **[TODO: exact product name and query parameters]** |
| Retrieval date | **[TODO: retrieval date]** |
| Station | A001, Brasília (DF), WMO 86715; 15.79° S, 47.93° W; elevation 1,161 m |
| File coverage | 2000-05-06 to 2025-04-25; 9,121 calendar days, no duplicate dates |
| Original fields | **[TODO: original BDMEP column names]** → `data`, `precipitacao_mm`, `temperatura_c`, `umidade_relativa_pct`, `vento_ms` |
| Daily-mean definition | Daily value supplied by INMET from hourly records; not recalculated by the authors **[TODO: confirm; specify hours and UTC time zone]** |
| Daily completeness criterion | **[TODO: INMET criterion for producing the daily value, if documented]** |
| Anemometer height | 10 m **[TODO: confirm against the station record]** |
| Sensor changes | Not documented in the file; not assessed |
| Recording step | 0.1 m/s (wind), 0.1 °C (temperature); file rounding, not metrological resolution |
| Wind gaps | 281 missing days; 101 gaps between valid records; longest gap 29 days |
| Authors' transformations | Column renaming and date conversion; no interpolation or missing-value imputation |
| Reading | “Read and inspect the data” cells of `distribuicoes_flexiveis_en.ipynb` |

The column names are retained in Portuguese in both notebooks to preserve the supplied CSV schema.
