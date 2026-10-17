"""Central configuration for the Climate Trend Analyzer."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIG_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"
REPORT_DIR = ROOT / "reports"

RAW_FILE = RAW_DIR / "climate_raw.csv"
CLEAN_FILE = PROCESSED_DIR / "climate_clean.csv"

START_YEAR = 1975
END_YEAR = 2024
SEED = 42

# Simulated regions: base temp (C), annual rain (mm), warming rate (C/decade), monsoon strength
REGIONS = {
    "Gujarat-West India": {"base_temp": 27.0, "rain": 800, "warm": 0.28, "monsoon": 1.0},
    "Northern Europe":    {"base_temp": 8.0,  "rain": 650, "warm": 0.35, "monsoon": 0.0},
    "Sahel Africa":       {"base_temp": 29.0, "rain": 450, "warm": 0.30, "monsoon": 0.8},
    "Pacific Coast US":   {"base_temp": 14.0, "rain": 900, "warm": 0.25, "monsoon": 0.0},
}

# Anomaly thresholds (z-scores). Tuned on the simulated data: temperature needs a stricter
# cut-off than rainfall because rainfall noise is heavy-tailed even after a log transform.
TEMP_Z_THRESHOLD = 3.0
RAIN_Z_THRESHOLD = 2.5      # extreme rainfall (upper tail)
DROUGHT_Z_THRESHOLD = 3.5   # very dry month (lower tail)
FORECAST_YEARS = 10
