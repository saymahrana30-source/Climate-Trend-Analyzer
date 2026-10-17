"""Long-term trend analysis: regression slopes, significance, STL decomposition."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

from src import config


def annual_table(df, value="temperature_c"):
    return df.groupby(["region", "year"])[value].mean().reset_index()


def trend_summary(df) -> pd.DataFrame:
    """Linear trend (°C per decade) + Kendall tau significance for each region."""
    rows = []
    ann = annual_table(df)
    for region, g in ann.groupby("region"):
        lr = stats.linregress(g["year"], g["temperature_c"])
        tau, p_mk = stats.kendalltau(g["year"], g["temperature_c"])
        rows.append({
            "region": region,
            "slope_c_per_decade": round(lr.slope * 10, 3),
            "r_squared": round(lr.rvalue ** 2, 3),
            "p_value": float(f"{lr.pvalue:.2e}"),
            "kendall_tau": round(tau, 3),
            "trend": "Warming" if lr.slope > 0 and lr.pvalue < 0.05 else "No significant trend",
        })
    out = pd.DataFrame(rows).sort_values("slope_c_per_decade", ascending=False)
    config.TABLE_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.TABLE_DIR / "trend_summary.csv", index=False)
    return out


def plot_trend_lines(df):
    ann = annual_table(df)
    regions = ann["region"].unique()
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)
    for ax, region in zip(axes.ravel(), regions):
        g = ann[ann["region"] == region]
        lr = stats.linregress(g["year"], g["temperature_c"])
        ax.scatter(g["year"], g["temperature_c"], s=22, color="#2e86ab")
        ax.plot(g["year"], lr.intercept + lr.slope * g["year"], color="#d1495b", linewidth=2)
        ax.set_title(f"{region}: {lr.slope*10:+.2f} °C/decade")
        ax.set_ylabel("Annual mean °C")
    fig.suptitle("Linear Warming Trend by Region", fontsize=14)
    config.FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = config.FIG_DIR / "09_trend_regression.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_decomposition(df, region):
    g = df[df["region"] == region].set_index("date")["temperature_c"].asfreq("MS")
    res = STL(g, period=12, robust=True).fit()
    fig = res.plot()
    fig.set_size_inches(12, 8)
    fig.suptitle(f"STL Decomposition - {region}", y=1.02)
    path = config.FIG_DIR / "10_stl_decomposition.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path, res


def run(df, focus_region="Gujarat-West India"):
    summary = trend_summary(df)
    plot_trend_lines(df)
    plot_decomposition(df, focus_region)
    return summary
