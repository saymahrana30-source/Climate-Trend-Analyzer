"""Interactive dashboard:  streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.express as px
import streamlit as st

from src import anomaly_detection, config, forecasting, trend_analysis
from src import data_generator, preprocessing

st.set_page_config(page_title="Climate Trend Analyzer", page_icon="🌍", layout="wide")


@st.cache_data
def load():
    if not config.CLEAN_FILE.exists():
        data_generator.save_raw()
        preprocessing.run()
    import pandas as pd
    return pd.read_csv(config.CLEAN_FILE, parse_dates=["date"])


df = load()
st.title("🌍 Climate Trend Analyzer")
st.caption("Simulated climate data, 1975-2024 | trends, anomalies, forecasts")

region = st.sidebar.selectbox("Region", sorted(df["region"].unique()))
years = st.sidebar.slider("Year range", int(df.year.min()), int(df.year.max()),
                          (int(df.year.min()), int(df.year.max())))
view = df[(df.region == region) & df.year.between(*years)]

trends = trend_analysis.trend_summary(df)
row = trends[trends.region == region].iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Warming rate", f"{row.slope_c_per_decade:+.2f} °C/decade")
c2.metric("Mean temperature", f"{view.temperature_c.mean():.1f} °C")
c3.metric("Avg annual rainfall", f"{view.groupby('year').rainfall_mm.sum().mean():.0f} mm")
c4.metric("CO₂ (latest)", f"{view.co2_ppm.iloc[-1]:.0f} ppm")

tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Seasonality", "Anomalies", "Forecast"])
with tab1:
    st.plotly_chart(px.line(view, x="date", y=["temperature_c", "temp_rolling_12m"],
                            title="Temperature (monthly vs 12-month rolling mean)"), width="stretch")
    ann = view.groupby("year").rainfall_mm.sum().reset_index()
    st.plotly_chart(px.bar(ann, x="year", y="rainfall_mm", title="Annual rainfall (mm)"), width="stretch")
with tab2:
    pivot = view.pivot_table(index="month", columns="year", values="temperature_c")
    st.plotly_chart(px.imshow(pivot, color_continuous_scale="RdBu_r", aspect="auto",
                              title="Monthly temperature heatmap"), width="stretch")
with tab3:
    scored = anomaly_detection.detect(df)
    table = anomaly_detection.anomaly_table(scored)
    st.dataframe(table[table.region == region], width="stretch")
    st.json(anomaly_detection.evaluate(scored))
with tab4:
    fc = forecasting.forecast_future(df, region)
    st.dataframe(fc, width="stretch")
    st.plotly_chart(px.line(fc, x="year", y=["linear_forecast_c", "arima_forecast_c"],
                            title="Forecast annual mean temperature"), width="stretch")
