"""Run with:  pytest -v"""
import numpy as np
import pandas as pd
import pytest

from src import anomaly_detection, config, data_generator, forecasting, preprocessing, trend_analysis


@pytest.fixture(scope="module")
def clean_df():
    raw = data_generator.generate_climate_data()
    return preprocessing.add_features(preprocessing.clean(raw))


def test_generator_shape_and_columns():
    raw = data_generator.generate_climate_data()
    assert {"date", "region", "temperature_c", "rainfall_mm", "co2_ppm"} <= set(raw.columns)
    assert raw["region"].nunique() == len(config.REGIONS)


def test_generator_is_reproducible():
    a = data_generator.generate_climate_data(seed=1)
    b = data_generator.generate_climate_data(seed=1)
    pd.testing.assert_frame_equal(a, b)


def test_cleaning_removes_problems(clean_df):
    assert clean_df[["temperature_c", "rainfall_mm", "humidity_pct"]].isna().sum().sum() == 0
    assert not clean_df.duplicated().any()
    assert (clean_df["temperature_c"] != -99).all()


def test_all_regions_warming(clean_df):
    t = trend_analysis.trend_summary(clean_df)
    assert (t["slope_c_per_decade"] > 0).all()
    assert (t["p_value"] < 0.05).all()


def test_anomaly_detection_quality(clean_df):
    scored = anomaly_detection.detect(clean_df)
    m = anomaly_detection.evaluate(scored)
    assert m["recall"] >= 0.8
    assert m["precision"] >= 0.7


def test_forecast_length_and_range(clean_df):
    fc = forecasting.forecast_future(clean_df, "Northern Europe")
    assert len(fc) == config.FORECAST_YEARS
    assert fc["arima_forecast_c"].between(5, 15).all()
