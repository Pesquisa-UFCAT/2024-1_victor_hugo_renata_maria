"""Published numerical anchors, unit conversion and calendar/scenario propagation."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

import functions as fn


class RecordingCarbonationModel:
    feature_names_in_ = ["t (years)", "CO2 (%)", "fc (MPa)", "RH (%)", "Type of cement", "Exposure conditions"]

    def predict(self, frame):
        self.frame = frame.copy()
        return np.zeros(len(frame))


class CO2Tests(unittest.TestCase):
    def test_published_table_5_values_in_percent(self):
        # Independent anchors: Table 5 of Meinshausen et al. (2020), global CO2 ppm.
        anchors = {"SSP1-2.6": (469.3, 445.6), "SSP2-4.5": (506.9, 602.8), "SSP5-8.5": (562.8, 1135.2)}
        for scenario, values in anchors.items():
            for year, ppm in zip((2050, 2100), values):
                with self.subTest(scenario=scenario, year=year):
                    self.assertAlmostEqual(fn.co2_percentage_year(year, scenario) * 10000, ppm, delta=.051)

    def test_common_history_and_boundaries(self):
        for year, ppm in [(1900, 295.675), (1980, 338.705), (2000, 369.125), (2014, 397.547)]:
            values = [fn.co2_percentage_year(year, s) for s in fn.CO2_SCENARIOS]
            self.assertEqual(len(set(values)), 1)
            self.assertAlmostEqual(values[0] * 10000, ppm, delta=.001)

    def test_linear_interpolation_at_history_scenario_join(self):
        for scenario in fn.CO2_SCENARIOS:
            expected = (fn.co2_percentage_year(2014, scenario) + fn.co2_percentage_year(2015, scenario)) / 2
            self.assertAlmostEqual(fn.co2_percentage_year(2014.5, scenario), expected, places=12)

    def test_default_and_compact_names(self):
        self.assertEqual(fn.co2_percentage_year(2100), fn.co2_percentage_year(2100, "SSP2-4.5"))
        for compact, canonical in zip(("ssp126", " ssp245 ", "ssp5-8.5"), fn.CO2_SCENARIOS):
            self.assertEqual(fn.co2_percentage_year(2100, compact), fn.co2_percentage_year(2100, canonical))

    def test_rejects_invalid_inputs_and_extrapolation(self):
        for year in (1899, 2100.1, np.nan, np.inf, True, "2050", None, [2050]):
            with self.subTest(year=year), self.assertRaises(ValueError):
                fn.co2_percentage_year(year)
        for scenario in ("RCP8.5", "SSP3-7.0", "", None, 245):
            with self.subTest(scenario=scenario), self.assertRaises(ValueError):
                fn.co2_percentage_year(1980, scenario)

    def test_local_data_independent_of_working_directory(self):
        previous = Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as directory:
                os.chdir(directory)
                fn._co2_concentrations.cache_clear()
                self.assertAlmostEqual(fn.co2_percentage_year(2100) * 10000, 602.8, delta=.051)
        finally:
            os.chdir(previous)

    def test_data_provenance_and_annual_completeness(self):
        folder = Path(fn.__file__).resolve().parent / "data/co2"
        metadata = json.loads((folder / "sources.json").read_text())
        csv = folder / "co2_concentrations_1900_2100.csv"
        self.assertEqual(hashlib.sha256(csv.read_bytes()).hexdigest(), metadata["csv_sha256"])
        data = pd.read_csv(csv)
        self.assertEqual(list(data.year), list(range(1900, 2101)))
        self.assertTrue(np.isfinite(data[list(fn.CO2_SCENARIOS)]).all().all())

    def test_structure_built_in_2000_reaches_2100_in_each_scenario(self):
        for scenario in fn.CO2_SCENARIOS:
            with self.subTest(scenario=scenario):
                model = RecordingCarbonationModel()
                full, unique = fn.emulator_function_time_durability(
                    np.array([[30., 65., 30.]]), ["fck", "rh", "cov"], model,
                    installation_year=2000, time_step=100, n_latent_samples=1, co2_scenario=scenario)
                self.assertEqual(model.frame["t (years)"].max(), 100)
                self.assertAlmostEqual(model.frame["CO2 (%)"].iloc[-1], fn.co2_percentage_year(2100, scenario))
                self.assertEqual(unique.attrs["co2_scenario"], scenario)
                self.assertEqual(full.attrs["co2_source"], "Meinshausen2017_2020")

    def test_fractional_endpoint_and_zero_duration(self):
        model = RecordingCarbonationModel()
        profile = fn.carbonation_profile(model, 99.5, 30, 65, 3, 2, 2000, co2_scenario="SSP1-2.6")
        self.assertEqual(profile["calendar year"].iloc[-1], 2099.5)
        self.assertAlmostEqual(profile["CO2 (%)"].iloc[-1], fn.co2_percentage_year(2099.5, "SSP1-2.6"))
        fn.emulator_function_time_durability(np.array([[30.,65.,30.]]), ["fck","rh","cov"], model,
                                            installation_year=2100, time_step=0, n_latent_samples=1)
        self.assertEqual(len(model.frame), 1)
        with self.assertRaises(ValueError):
            fn.carbonation_profile(model, 101, 30, 65, 3, 2, 2000)

    def test_saved_scenarios_do_not_overwrite_each_other(self):
        paths = []
        with tempfile.TemporaryDirectory() as directory:
            for scenario in fn.CO2_SCENARIOS:
                result = fn.generate_dataset_at_time_durability(
                    np.array([[30.,65.,30.]]), np.array([[35.,60.,35.]]), RecordingCarbonationModel(),
                    time_step=100, installation_year=2000, n_latent_samples=1,
                    co2_scenario=scenario, output_dir=directory, verbose=False)
                path = result["paths"]["dataset_unique_train"]
                self.assertIn(scenario, path.name)
                self.assertTrue(path.exists())
                paths.append(path)
            self.assertEqual(len(set(paths)), 3)

    def test_rejects_old_or_mismatched_datasets_before_training(self):
        for metadata in ({}, {"co2_scenario":"SSP5-8.5", "co2_source":"Meinshausen2017_2020"}):
            frame = pd.DataFrame()
            frame.attrs.update(metadata)
            with self.assertRaisesRegex(ValueError, "Regenerate"):
                fn.train_and_validate_pce_from_dataset_durability(frame, frame, None, 50, verbose=False)


if __name__ == "__main__":
    unittest.main()
