"""Virtual simulation: builds a realistic synthetic monthly climate dataset.

Why synthetic? Real institutional data is not needed - this mimics what NASA/NOAA-style
station data looks like (seasonality + long-term warming + noise + messy values) so the whole
analysis pipeline can be demonstrated end to end.
"""
import numpy as np
import pandas as pd

from src import config


def generate_climate_data(seed: int = config.SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(f"{config.START_YEAR}-01-01", f"{config.END_YEAR}-12-01", freq="MS")
    n = len(dates)
    years_elapsed = (dates.year - config.START_YEAR) + (dates.month - 1) / 12
    month = dates.month.to_numpy()
    frames = []

    # Global indicators (same for all regions)
    co2 = 331 + 1.45 * years_elapsed + 0.012 * years_elapsed**2 \
        + 3.0 * np.sin(2 * np.pi * (month - 4) / 12) + rng.normal(0, 0.3, n)
    sea_level = 5.0 * years_elapsed + 0.04 * years_elapsed**2 + rng.normal(0, 3.0, n)

    for region, p in config.REGIONS.items():
        seasonal_amp = 12.0 if p["base_temp"] < 15 else 6.0
        # Temperature = base + seasonal cycle + warming trend + noise
        temp = (p["base_temp"]
                + seasonal_amp * np.sin(2 * np.pi * (month - 4) / 12)
                + p["warm"] / 10 * years_elapsed
                + rng.normal(0, 0.9, n))

        # Rainfall: monsoon regions peak Jun-Sep, others spread evenly with mild winter bias
        monthly_mean = p["rain"] / 12
        if p["monsoon"] > 0:
            shape = 1 + 2.6 * p["monsoon"] * np.exp(-((month - 7.5) ** 2) / 4.0) - 0.7 * p["monsoon"]
        else:
            shape = 1 + 0.35 * np.cos(2 * np.pi * (month - 1) / 12)
        shape = np.clip(shape, 0.05, None)
        rain = monthly_mean * shape * rng.gamma(4.0, 0.25, n)

        humidity = np.clip(50 + 0.08 * rain + 6 * np.sin(2 * np.pi * (month - 7) / 12)
                           + rng.normal(0, 4, n), 15, 99)

        df = pd.DataFrame({
            "date": dates, "region": region,
            "temperature_c": temp.round(2), "rainfall_mm": rain.round(1),
            "humidity_pct": humidity.round(1),
            "co2_ppm": co2.round(2), "sea_level_mm": sea_level.round(1),
        })

        # Inject genuine extreme events (heatwaves / cold snaps / floods) -> ground truth anomalies
        idx = rng.choice(n, size=6, replace=False)
        df["is_injected_anomaly"] = 0
        for k, i in enumerate(idx):
            if k % 3 == 0:
                df.loc[i, "temperature_c"] += rng.uniform(6, 9)   # heatwave
            elif k % 3 == 1:
                df.loc[i, "temperature_c"] -= rng.uniform(6, 9)   # cold snap
            else:
                df.loc[i, "rainfall_mm"] *= rng.uniform(3.5, 5)   # extreme rainfall
            df.loc[i, "is_injected_anomaly"] = 1
        frames.append(df)

    full = pd.concat(frames, ignore_index=True)

    # Make the data MESSY like the real world: missing values, sentinel errors, duplicates
    miss_idx = rng.choice(len(full), size=int(0.02 * len(full)), replace=False)
    full.loc[miss_idx, "temperature_c"] = np.nan
    miss_idx = rng.choice(len(full), size=int(0.02 * len(full)), replace=False)
    full.loc[miss_idx, "rainfall_mm"] = np.nan
    miss_idx = rng.choice(len(full), size=int(0.015 * len(full)), replace=False)
    full.loc[miss_idx, "humidity_pct"] = np.nan
    bad_idx = rng.choice(len(full), size=8, replace=False)
    full.loc[bad_idx, "temperature_c"] = -99.0           # sensor error code
    dupes = full.sample(25, random_state=seed)
    full = pd.concat([full, dupes], ignore_index=True).sample(frac=1, random_state=seed)
    return full.reset_index(drop=True)


def save_raw() -> pd.DataFrame:
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_climate_data()
    df.to_csv(config.RAW_FILE, index=False)
    return df


if __name__ == "__main__":
    d = save_raw()
    print(f"Saved {len(d)} rows to {config.RAW_FILE}")
