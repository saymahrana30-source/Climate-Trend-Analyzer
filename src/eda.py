"""Exploratory data analysis: publication-style charts saved to outputs/figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src import config

sns.set_theme(style="whitegrid", context="notebook")


def _save(fig, name):
    config.FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = config.FIG_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def temperature_trend(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for region, g in df.groupby("region"):
        ax.plot(g["date"], g["temp_rolling_12m"], label=region, linewidth=1.8)
    ax.set(title="Temperature Trend by Region (12-month rolling mean)", xlabel="Year", ylabel="Temperature (°C)")
    ax.legend()
    return _save(fig, "01_temperature_trend.png")


def rainfall_trend(df):
    annual = df.groupby(["year", "region"])["rainfall_mm"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=annual, x="year", y="rainfall_mm", hue="region", ax=ax)
    ax.set(title="Annual Rainfall by Region", xlabel="Year", ylabel="Total rainfall (mm)")
    return _save(fig, "02_rainfall_trend.png")


def seasonal_pattern(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.lineplot(data=df, x="month", y="temperature_c", hue="region", errorbar=None, ax=axes[0])
    axes[0].set(title="Average Monthly Temperature", xlabel="Month", ylabel="°C")
    sns.lineplot(data=df, x="month", y="rainfall_mm", hue="region", errorbar=None, ax=axes[1])
    axes[1].set(title="Average Monthly Rainfall", xlabel="Month", ylabel="mm")
    return _save(fig, "03_seasonal_pattern.png")


def monthly_heatmap(df, region):
    g = df[df["region"] == region]
    pivot = g.pivot_table(index="month", columns="year", values="temperature_c")
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.heatmap(pivot, cmap="coolwarm", ax=ax, cbar_kws={"label": "°C"})
    ax.set_title(f"Monthly Temperature Heatmap - {region}")
    return _save(fig, "04_monthly_heatmap.png")


def yearly_comparison(df):
    first = df[df["year"].between(config.START_YEAR, config.START_YEAR + 9)]
    last = df[df["year"].between(config.END_YEAR - 9, config.END_YEAR)]
    comp = (last.groupby("region")["temperature_c"].mean()
            - first.groupby("region")["temperature_c"].mean()).sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    comp.plot(kind="barh", color="#d1495b", ax=ax)
    ax.set(title=f"Warming: {config.END_YEAR-9}-{config.END_YEAR} vs {config.START_YEAR}-{config.START_YEAR+9}",
           xlabel="Change in mean temperature (°C)", ylabel="")
    for i, v in enumerate(comp):
        ax.text(v + 0.01, i, f"+{v:.2f}", va="center")
    return _save(fig, "05_yearly_comparison.png")


def co2_vs_temperature(df):
    annual = df.groupby("year").agg(temp=("temperature_c", "mean"), co2=("co2_ppm", "mean")).reset_index()
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.regplot(data=annual, x="co2", y="temp", ax=ax, color="#2e86ab")
    r = annual["co2"].corr(annual["temp"])
    ax.set(title=f"CO₂ vs Temperature (r = {r:.2f})", xlabel="CO₂ (ppm)", ylabel="Mean temperature (°C)")
    return _save(fig, "06_co2_vs_temperature.png")


def correlation_heatmap(df):
    cols = ["temperature_c", "rainfall_mm", "humidity_pct", "co2_ppm", "sea_level_mm"]
    annual = df.groupby("year")[cols].mean()   # annual means remove the monthly seasonal cycle
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(annual.corr(), annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Correlation Matrix of Climate Variables (annual means)")
    return _save(fig, "07_correlation_heatmap.png")


def sea_level_plot(df):
    g = df.groupby("year")["sea_level_mm"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(g.index, g.values, color="#0b3d91", linewidth=2)
    ax.fill_between(g.index, g.values, g.values.min(), alpha=0.15, color="#0b3d91")
    ax.set(title="Simulated Sea Level Rise", xlabel="Year", ylabel="Sea level (mm, relative)")
    return _save(fig, "08_sea_level_rise.png")


def run_all(df, focus_region="Gujarat-West India"):
    return [temperature_trend(df), rainfall_trend(df), seasonal_pattern(df),
            monthly_heatmap(df, focus_region), yearly_comparison(df),
            co2_vs_temperature(df), correlation_heatmap(df), sea_level_plot(df)]
