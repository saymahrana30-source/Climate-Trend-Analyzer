"""Generates a plain-language insights report (Markdown) from the analysis results."""
from datetime import date

from src import config


def build_report(df, trends, anomalies, anomaly_metrics, forecast_metrics, forecasts) -> str:
    hottest = trends.iloc[0]
    co2_corr = df.groupby("year").agg(t=("temperature_c", "mean"), c=("co2_ppm", "mean")).corr().iloc[0, 1]
    sea_rise = df.groupby("year")["sea_level_mm"].mean()
    best = forecast_metrics.groupby("model")["RMSE"].mean().sort_values()
    fc_end = forecasts[forecasts["year"] == forecasts["year"].max()]

    lines = [
        "# Climate Trend Analyzer - Insights Report",
        f"_Generated on {date.today():%d %b %Y} from simulated data ({config.START_YEAR}-{config.END_YEAR})_",
        "",
        "## Key Findings",
        f"1. **{(trends['trend'] == 'Warming').sum()} of {len(trends)} regions show statistically significant warming.** "
        f"Fastest: **{hottest['region']}** at **{hottest['slope_c_per_decade']:+.2f} °C/decade**.",
        f"2. **CO₂ and temperature are strongly correlated** (r = {co2_corr:.2f} on annual means).",
        f"3. **Sea level rose ~{sea_rise.iloc[-1] - sea_rise.iloc[0]:.0f} mm** over the period (simulated).",
        f"4. **{len(anomalies)} anomalous months** flagged "
        f"(precision {anomaly_metrics['precision']:.0%}, recall {anomaly_metrics['recall']:.0%} against injected events).",
        f"5. **Best forecaster:** {best.index[0]} (mean RMSE {best.iloc[0]:.3f} °C on a 10-year holdout).",
        "",
        "## Trend Table",
        trends.to_markdown(index=False),
        "",
        f"## Forecast for {int(fc_end['year'].iloc[0])} (ARIMA)",
        fc_end[["region", "arima_forecast_c", "arima_lower_95", "arima_upper_95"]].to_markdown(index=False),
        "",
        "## Who Can Use This",
        "- **Agritech:** shift crop calendars as seasonal rainfall patterns move.",
        "- **Energy:** plan cooling demand using regional warming rates.",
        "- **Urban planning:** use extreme-event frequency to size drainage and heat-action plans.",
        "",
        "> Note: data is simulated for demonstration. Swap in NASA GISTEMP / NOAA CSVs "
        "with the same column names to analyse real records.",
    ]
    return "\n".join(lines)


def save_report(text: str):
    config.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = config.REPORT_DIR / "insights_report.md"
    path.write_text(text, encoding="utf-8")
    return path
