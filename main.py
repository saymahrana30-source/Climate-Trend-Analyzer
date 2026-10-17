"""Run the full Climate Trend Analyzer pipeline:  python main.py"""
import argparse

import pandas as pd

from src import (anomaly_detection, config, data_generator, eda, forecasting,
                 preprocessing, report, trend_analysis)

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 20)


def banner(text):
    print(f"\n{'=' * 64}\n  {text}\n{'=' * 64}")


def main(focus_region: str):
    banner("STEP 1/6  Generating simulated climate dataset")
    raw = data_generator.save_raw()
    print(f"Saved {len(raw):,} rows -> {config.RAW_FILE.relative_to(config.ROOT)}")
    print(raw.head())

    banner("STEP 2/6  Cleaning & preprocessing")
    print("Data quality BEFORE cleaning:")
    for k, v in preprocessing.data_quality_report(raw).items():
        print(f"  {k:<16}: {v}")
    df = preprocessing.run()
    print(f"\nClean rows: {len(df):,} | remaining missing: "
          f"{int(df[['temperature_c', 'rainfall_mm', 'humidity_pct']].isna().sum().sum())}")
    print(f"Saved -> {config.CLEAN_FILE.relative_to(config.ROOT)}")

    banner("STEP 3/6  Exploratory data analysis")
    for p in eda.run_all(df, focus_region):
        print(f"  saved {p.relative_to(config.ROOT)}")

    banner("STEP 4/6  Long-term trend analysis")
    trends = trend_analysis.run(df, focus_region)
    print(trends.to_string(index=False))

    banner("STEP 5/6  Anomaly detection")
    scored, anomalies, metrics = anomaly_detection.run(df)
    print(f"Anomalous months flagged: {len(anomalies)}")
    print(anomalies.head(10).to_string(index=False))
    print(f"\nEvaluation vs injected events: {metrics}")

    banner("STEP 6/6  Forecasting & report")
    fmetrics, forecasts = forecasting.run(df, focus_region)
    print(fmetrics.to_string(index=False))
    text = report.build_report(df, trends, anomalies, metrics, fmetrics, forecasts)
    path = report.save_report(text)
    print(f"\nReport saved -> {path.relative_to(config.ROOT)}")
    banner("DONE - outputs in outputs/figures, outputs/tables, reports/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Climate Trend Analyzer")
    ap.add_argument("--region", default="Gujarat-West India", choices=list(config.REGIONS))
    main(ap.parse_args().region)
