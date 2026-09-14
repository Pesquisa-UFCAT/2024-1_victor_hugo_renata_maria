"""Generate the paper's CO2 and reference carbonation figures in PT and EN.

Run with the project's Python. Uses the local CO2 table and functions.py.
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions import CO2_SCENARIOS, carbonation_depth_possan_by_type, co2_percentage_year

PAPER = ROOT / "texto/artigo"
OUTPUT = ROOT / "artifacts/co2_scenarios"
COLORS = ("#00866b", "#2673b8", "#c74634")
STYLES = ("--", "-", "-.")
TEXT = {
    "pt": {"year": "Ano", "co2": r"Concentração de CO$_2$ (ppm)",
           "history": "Histórico (1980–2014)", "age": "Idade da estrutura (anos)",
           "depth": "Profundidade de\ncarbonatação (mm)", "cover": "Cobrimento: 30 mm", "rh": "UR"},
    "en": {"year": "Year", "co2": r"CO$_2$ concentration (ppm)",
           "history": "Historical (1980–2014)", "age": "Structure age (years)",
           "depth": "Carbonation depth (mm)", "cover": "Concrete cover: 30 mm", "rh": "RH"},
}


def new_axes():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.tick_params(labelsize=12)
    ax.grid(True, linestyle="--", color="0.88", linewidth=.8)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    fig.tight_layout()
    for extension in ("png", "pdf", "svg"):
        fig.savefig(PAPER / f"{name}.{extension}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 12,
                         "axes.labelsize": 14, "axes.unicode_minus": False,
                         "axes.spines.top": True, "axes.spines.right": True, "pdf.fonttype": 42,
                         "legend.fontsize": 10, "legend.framealpha": 1, "legend.edgecolor": "0.8"})
    years = np.arange(1980, 2101)
    values = {scenario: np.array([co2_percentage_year(int(y), scenario) * 10000 for y in years])
              for scenario in CO2_SCENARIOS}
    csv = pd.DataFrame({"year": years, **{f"{s}_ppm": v for s, v in values.items()}})
    csv.to_csv(OUTPUT / "co2_1980_2100.csv", index=False, float_format="%.9f")

    # Reference profiles: structure built in 2000, SSP2-4.5, CP II F,
    # protected external exposure, ad=10%. Instantaneous evaluation plus cummax,
    # as in the existing profile convention; this is not an exposure integral.
    ages = np.arange(0, 101)
    concentration = np.array([co2_percentage_year(2000 + int(age), "SSP2-4.5") for age in ages])
    profiles = pd.DataFrame({"age_years": ages, "calendar_year": 2000 + ages, "co2_percent": concentration})
    for fc in (20, 30, 40, 50):
        profiles[f"fck_{fc}_rh_65_mm"] = np.maximum.accumulate(carbonation_depth_possan_by_type(
            fc, ages, .65, concentration, cement_type=3, exposure_conditions=2, ad=10.0))
    for rh in (50, 65, 80):
        profiles[f"fck_30_rh_{rh}_mm"] = np.maximum.accumulate(carbonation_depth_possan_by_type(
            30, ages, rh / 100, concentration, cement_type=3, exposure_conditions=2, ad=10.0))
    profiles.to_csv(OUTPUT / "carbonation_reference_2000_2100.csv", index=False, float_format="%.9f")

    for language, text in TEXT.items():
        fig, ax = new_axes()
        historic = years <= 2014
        ax.plot(years[historic], values["SSP2-4.5"][historic], color="black", lw=1.8, label=text["history"])
        future = years >= 2014  # join the last historical point to the 2015 SSP value
        for scenario, color, style in zip(CO2_SCENARIOS, COLORS, STYLES):
            ax.plot(years[future], values[scenario][future], color=color, ls=style, lw=1.9, label=scenario)
        ax.axvline(2014.5, color=".65", lw=.9, ls=":")
        ax.set(xlim=(1980, 2100), ylim=(300, 1200), xlabel=text["year"], ylabel=text["co2"])
        ax.set_xticks(np.arange(1980, 2101, 20))
        ax.set_yticks(np.arange(300, 1201, 150))
        ax.legend(loc="upper left")
        save(fig, f"z_co2_scenarios_{language}")

        for variable in ("fck", "rh"):
            fig, ax = new_axes()
            settings = (20, 30, 40, 50) if variable == "fck" else (50, 65, 80)
            for i, value in enumerate(settings):
                column = f"fck_{value}_rh_65_mm" if variable == "fck" else f"fck_30_rh_{value}_mm"
                label = rf"$f_c = {value}$ MPa" if variable == "fck" else f"{text['rh']} = {value}%"
                ax.plot(ages, profiles[column], color=("black", *COLORS)[i],
                        ls=("-", "--", "-.", ":")[i], lw=1.7, label=label)
            ax.axhline(30, color=".45", lw=1.1, ls="--", label=text["cover"])
            ax.set(xlim=(0, 100), ylim=(0, 80), xlabel=text["age"], ylabel=text["depth"])
            ax.legend(loc="upper left", fontsize=9)
            save(fig, f"z_carbonation_{variable}_{language}")
    print(csv[csv.year.isin([2050, 2080, 2100])].to_string(index=False))


if __name__ == "__main__":
    main()
