# 📈 End-to-End Real-Time Stock Anomaly Detection System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_APP_LINK_HERE)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview
This project is a deployed web application that monitors live stock market data and utilizes statistical algorithms to automatically flag abnormal price behaviors.

By implementing a **Sliding Window Algorithm** and **Z-Score Analysis**, the system identifies significant market deviations (crashes or spikes) in real-time, helping users distinguish between standard market volatility and critical anomalies.

**[👉 View the Live App Here](https://5ykp2myc3hbxkwygoohw5k.streamlit.app/)**

---

## ⚙️ How It Works (The Logic)

This application follows a strict data engineering pipeline to ensure accuracy:

1.  **Data Ingestion:** The app fetches real-time historical data from the **Yahoo Finance API (`yfinance`)**.
2.  **Data Processing (DSA):** A **Sliding Window Algorithm** (window size = 20 days) is used to process time-series data efficiently.
3.  **Statistical Logic:**
    * For every data point, the system calculates the **Moving Average ($\mu$)** and **Standard Deviation ($\sigma$)** within the window.
    * It then computes the **Z-Score**:
        $$Z = \frac{X - \mu}{\sigma}$$
4.  **Anomaly Detection:**
    * **Logic:** If the Z-Score is **> 3** or **< -3**, the price is statistically significant.
    * **Outcome:** The system flags this data point as an "Anomaly" on the dashboard.
5.  **Visualization:** Results are plotted interactively using **Plotly Express**, allowing users to zoom in on specific dates and anomalies.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Processing:** Pandas (Data manipulation, Rolling Window functions)
* **API:** yfinance (Live market data fetcher)
* **Visualization:** Plotly Express (Interactive charting)
* **Frontend/UI:** Streamlit (Web interface)
* **Deployment:** Streamlit Cloud + GitHub Actions



