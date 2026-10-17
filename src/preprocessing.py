"""Data cleaning: duplicates, sentinel errors, dates, missing values, features."""
import numpy as np
import pandas as pd

from src import config

SENTINEL = -99.0


def load_raw(path=config.RAW_FILE) -> pd.DataFrame:
    return pd.read_csv(path)


def data_quality_report(df: pd.DataFrame) -> dict:
    """Snapshot of how messy the raw data is (used for the preprocessing screenshot)."""
    return {
        "rows": len(df),
        "duplicates": int(df.duplicated().sum()),
        "missing": df[["temperature_c", "rainfall_mm", "humidity_pct"]].isna().sum().to_dict(),
        "sentinel_errors": int((df["temperature_c"] == SENTINEL).sum()),
    }


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).drop_duplicates()
    df.loc[df["temperature_c"] == SENTINEL, "temperature_c"] = np.nan   # sensor error code -> NaN
    df = df.sort_values(["region", "date"]).reset_index(drop=True)

    cols = ["temperature_c", "rainfall_mm", "humidity_pct"]
    for region, grp in df.groupby("region"):
        # time-aware interpolation inside each region, then fill any edge gaps
        filled = grp.set_index("date")[cols].interpolate(method="time").bfill().ffill()
        df.loc[grp.index, cols] = filled.values.round(2)
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].map(
        {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
         6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"})
    df["temp_rolling_12m"] = df.groupby("region")["temperature_c"].transform(
        lambda s: s.rolling(12, min_periods=12).mean())
    return df


def run() -> pd.DataFrame:
    raw = load_raw()
    clean_df = add_features(clean(raw))
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(config.CLEAN_FILE, index=False)
    return clean_df
