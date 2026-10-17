# Screenshots

Proof of the project running. Terminal shots show real output of the commands listed; code shots show the actual source files.

## terminal/
| File | Command | Shows |
|---|---|---|
| 01_environment_check.png | `python -c "import pandas, ..."` | Python + library versions |
| 02_project_structure.png | `tree` | Final folder layout |
| 03_dataset_preview.png | `df.head(); df.info()` | Raw dataset preview |
| 04_missing_values_check.png | `df.isnull().sum()` | Missing values, duplicates, sensor errors |
| 05-10_pipeline_step*.png | `python main.py` | Each of the 6 pipeline steps |
| 11_full_pipeline_run_summary.png | `python main.py --region "Sahel Africa"` | Condensed full run |
| 12_pytest_results.png | `pytest -v` | 6/6 tests passing |
| 13_streamlit_dashboard_launch.png | `streamlit run app/streamlit_app.py` | Dashboard launch |

## code/
01 config · 02 data_generator · 03 preprocessing · 04 trend_analysis · 05 anomaly_detection · 06 forecasting · 07 main · 08 streamlit_app · 09 tests
