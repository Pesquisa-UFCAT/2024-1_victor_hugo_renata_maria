"""Standalone extract of the Possan et al. (2016) carbonation model from the repo functions.py
(2024-1_victor_hugo_renata_maria). Verbatim coefficient tables and model; CO2 loader reads the CSV path given.
"""
import numpy as np, pandas as pd
POSSAN_CEMENT_COEFFICIENTS = {
                                 0: {'name': 'CP II Z',  'k_c': 23.66, 'k_fc': 1.50, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 1: {'name': 'CP V-ARI', 'k_c': 19.80, 'k_fc': 1.70, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1300.0},
                                 2: {'name': 'CP IV',    'k_c': 33.27, 'k_fc': 1.70, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1000.0},
                                 3: {'name': 'CP II F',  'k_c': 21.68, 'k_fc': 1.50, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1100.0},
                                 4: {'name': 'CP III',   'k_c': 30.50, 'k_fc': 1.70, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 5: {'name': 'CP II E',  'k_c': 22.48, 'k_fc': 1.50, 'k_ad': 0.32, 'k_co_2': 15.50, 'k_rh': 1300.0},
                                 6: {'name': 'CP I',     'k_c': 19.80, 'k_fc': 1.70, 'k_ad': 0.24, 'k_co_2': 18.00, 'k_rh': 1300.0},
                             }

# Possan et al. (2016) carbonation model coefficients, Table 3b — exposure condition factor,
# keyed by the `exposure_conditions` encoding used throughout this pipeline.
POSSAN_EXPOSURE_COEFFICIENTS = {
                                   0: {'name': 'PIA — internal, protected from rain', 'k_ce': 1.30},
                                   1: {'name': 'UEA — external, exposed to rain',     'k_ce': 0.65},
                                   2: {'name': 'PEA — external, protected from rain', 'k_ce': 1.00},
                               }


def possan_coefficients(cement_type: int = 3, exposure_conditions: int = 2) -> dict:
    """Looks up the six Possan et al. (2016) model coefficients for a given cement type and exposure condition, combining Tables 3a and 3b.

    :param cement_type: Type of cement (0: CP II Z, 1: CP V-ARI, 2: CP IV, 3: CP II F, 4: CP III, 5: CP II E, 6: CP I)
    :param exposure_conditions: Exposure conditions (0: PIA internal protected, 1: UEA external unprotected, 2: PEA external protected)

    :return: Dictionary with the coefficients k_c, k_fc, k_ad, k_co_2, k_rh and k_ce, plus the descriptive names
    """

    if cement_type not in POSSAN_CEMENT_COEFFICIENTS:
        raise ValueError(f"Unknown cement_type {cement_type}. Valid values: {sorted(POSSAN_CEMENT_COEFFICIENTS)}")
    if exposure_conditions not in POSSAN_EXPOSURE_COEFFICIENTS:
        raise ValueError(f"Unknown exposure_conditions {exposure_conditions}. Valid values: {sorted(POSSAN_EXPOSURE_COEFFICIENTS)}")

    cement   = POSSAN_CEMENT_COEFFICIENTS[cement_type]
    exposure = POSSAN_EXPOSURE_COEFFICIENTS[exposure_conditions]

    return {
               'k_c':           cement['k_c'],
               'k_fc':          cement['k_fc'],
               'k_ad':          cement['k_ad'],
               'k_co_2':        cement['k_co_2'],
               'k_rh':          cement['k_rh'],
               'k_ce':          exposure['k_ce'],
               'cement_name':   cement['name'],
               'exposure_name': exposure['name'],
           }


def carbonation_depth_possan(f_ck: np.ndarray | float, t: np.ndarray | float, ur: np.ndarray | float, co_2: np.ndarray | float, k_c: float, k_fc: float, k_ad: float, k_co_2: float, k_rh: float, k_ce: float, ad: np.ndarray | float = 0.0) -> np.ndarray | float:
    r"""Carbonation depth of concrete according to the model of Possan et al. (2016), https://doi.org/10.1007/s41024-016-0010-9.

    .. math::

        y(t) = k_c \left(\frac{20}{f_{ck}}\right)^{k_{fc}} \left(\frac{t}{20}\right)^{1/2}
               \exp\left[\frac{k_{ad}\,ad^{3/2}}{40 + f_{ck}}
                       + \frac{k_{CO_2}\sqrt{CO_2}}{60 + f_{ck}}
                       - \frac{k_{UR}(UR - 0.58)^2}{100 + f_{ck}}\right] k_{ce}

    Fully vectorized: every physical argument accepts a scalar or a numpy array, and broadcasting
    rules apply. This is the closed-form simulator of the durability pipeline — it replaces the
    surrogate ML model used previously, so the emulator is trained against the mechanistic model
    itself rather than against an approximation of it.

    Unit conventions, which differ from the original single-point implementation:

    - the result is returned in **millimetres**, matching the concrete cover used elsewhere in this
      pipeline (`g = cover - carbonation depth` is therefore a mm - mm difference);
    - `ur` is a **fraction** in [0, 1] (0.70 for 70% RH), not a percentage. The quadratic term peaks
      at UR = 0.58, i.e. carbonation is fastest around 58% relative humidity. Passing a percentage
      here silently produces a meaningless depth, so values above 1.5 raise.

    The caller is responsible for keeping `f_ck` strictly positive and `ur` within physical bounds
    after any latent perturbation, as `emulator_function_time_durability` already does by clipping.

    .. note::

        The synthetic dataset behind the previously used ML surrogate was generated with
        ``ad = 10`` (%). Calling this function with the default ``ad = 0`` reproduces neither that
        dataset nor the earlier durability results: depths come out roughly 1.6 mm shallower.
        Pass ``ad=10.0`` to stay consistent with the existing pipeline. Checked against the
        surrogate over the full input box: bias +0.05 mm, standard deviation 0.30 mm,
        R2 = 0.999 at ``ad = 10``, against bias +1.64 mm and R2 = 0.978 at ``ad = 0``.

    :param f_ck: Characteristic compressive strength of the concrete (MPa)
    :param t: Age of the structure (years)
    :param ur: Mean relative humidity, as a fraction in [0, 1]
    :param co_2: Atmospheric CO2 concentration (%)
    :param k_c: Factor related to the cement type (Table 3a)
    :param k_fc: Factor related to the compressive strength of the concrete (Table 3a)
    :param k_ad: Factor related to the pozzolanic additions of the concrete (Table 3a)
    :param k_co_2: Factor related to the CO2 concentration of the environment (Table 3a)
    :param k_rh: Factor related to the relative humidity (Table 3a)
    :param k_ce: Factor related to the exposure condition of the structure (Table 3b)
    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%)

    :return: Carbonation depth (mm)
    """

    f_ck = np.asarray(f_ck, dtype=float)
    t    = np.asarray(t, dtype=float)
    ur   = np.asarray(ur, dtype=float)
    co_2 = np.asarray(co_2, dtype=float)
    ad   = np.asarray(ad, dtype=float)

    if np.any(ur > 1.5):
        raise ValueError("`ur` must be a fraction in [0, 1] (0.70 for 70% RH), not a percentage.")

    aux_1  = k_c * (20.0 / f_ck) ** k_fc
    aux_2  = (t / 20.0) ** 0.5
    aux_31 = (k_ad * ad ** 1.5) / (40.0 + f_ck)
    aux_32 = (k_co_2 * co_2 ** 0.5) / (60.0 + f_ck)
    aux_33 = (k_rh * (ur - 0.58) ** 2) / (100.0 + f_ck)
    y_carb = aux_1 * aux_2 * np.exp(aux_31 + aux_32 - aux_33) * k_ce

    return y_carb


def carbonation_depth_possan_by_type(f_ck: np.ndarray | float, t: np.ndarray | float, ur: np.ndarray | float, co_2: np.ndarray | float, cement_type: int = 3, exposure_conditions: int = 2, ad: np.ndarray | float = 0.0) -> np.ndarray | float:
    """Convenience wrapper around `carbonation_depth_possan` that looks the six model coefficients up from the cement type and exposure condition, using the integer encodings adopted throughout this pipeline.

    :param f_ck: Characteristic compressive strength of the concrete (MPa)
    :param t: Age of the structure (years)
    :param ur: Mean relative humidity, as a fraction in [0, 1]
    :param co_2: Atmospheric CO2 concentration (%)
    :param cement_type: Type of cement (0: CP II Z, 1: CP V-ARI, 2: CP IV, 3: CP II F, 4: CP III, 5: CP II E, 6: CP I)
    :param exposure_conditions: Exposure conditions (0: PIA internal protected, 1: UEA external unprotected, 2: PEA external protected)
    :param ad: Pozzolanic material in the concrete, relative to the cement mass (%)

    :return: Carbonation depth (mm)
    """

    coefficients = possan_coefficients(cement_type=cement_type, exposure_conditions=exposure_conditions)

    return carbonation_depth_possan(
                                       f_ck=f_ck, t=t, ur=ur, co_2=co_2, ad=ad,
                                       k_c=coefficients['k_c'], k_fc=coefficients['k_fc'], k_ad=coefficients['k_ad'],
                                       k_co_2=coefficients['k_co_2'], k_rh=coefficients['k_rh'], k_ce=coefficients['k_ce'],
                                   )



def load_co2(csv_path):
    """Annual CO2 (ppm) table with columns year, SSP1-2.6, SSP2-4.5, SSP5-8.5 (1900-2100)."""
    return pd.read_csv(csv_path)

def co2_percent(df, year, scenario="SSP2-4.5"):
    """CO2 in percent (ppm/1e4), linear interpolation in calendar year, as in the repo."""
    return np.interp(year, df["year"].values, df[scenario].values) / 1e4
