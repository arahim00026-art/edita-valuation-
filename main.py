import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Edita Financial Intelligence", layout="wide")

# --- ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background */
    .main { background-color: #f8f9fa; }
    
    /* KPI Card Styling - white Font Fix */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 700;
        font-size: 2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: 500;
    }
    
    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #666666;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #eaeaea;
        z-index: 999;
    }
    
    /* Metric Container */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍰 Edita Food Industries: Strategic Performance Review")
st.markdown("---")

# --- SIDEBAR: DYNAMIC ASSUMPTIONS ---
st.sidebar.header("🕹️ Scenario Manager")
st.sidebar.info("Adjust metrics to simulate economic shifts.")
rev_growth = st.sidebar.slider("Revenue Growth (%)", 0.05, 0.45, 0.20)
wacc = st.sidebar.slider("WACC / Hurdle Rate (%)", 0.10, 0.25, 0.18)

# --- DATA ENGINE ---
df_hist = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024, 2025],
    'Revenue': [5.25, 7.67, 12.12, 16.15, 20.92],
    'Gross_Margin': [31.2, 29.8, 32.5, 30.4, 33.9],
    'Net_Margin': [10.1, 9.5, 9.2, 8.8, 11.7]
})

# Forecast Logic
current_rev = 20.92
forecast = []
for year in range(2026, 2031):
    current_rev *= (1 + rev_growth)
    forecast.append({'Year': year, 'Revenue': current_rev})
df_forecast = pd.DataFrame(forecast)

# --- TOP ROW: KPI METRICS (Now in Bold Black) ---
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("FY25 Revenue", "20.9B EGP", "+29.5%")
m_col2.metric("Net Margin", "11.7%", "+2.9% bps")
m_col3.metric("ROE (Actual)", "39.9%", "High Rank")
m_col4.metric("Current Ratio", "1.27x", "Stable")

# --- TABBED ANALYSIS ---
tab1, tab2, tab3 = st.tabs(["📊 Growth & Profitability", "🛡️ Risk & Liquidity", "💎 Equity Valuation"])

with tab1:
    st.subheader("Historical vs. Projected Revenue")
    st.area_chart(pd.concat([df_hist[['Year', 'Revenue']], df_forecast]).set_index('Year'), color="#005a9c")
    
    st.markdown("---")
    st.subheader("Margin Expansion Analysis (%)")
    st.line_chart(df_hist.set_index('Year')[['Gross_Margin', 'Net_Margin']], color=["#2ca02c", "#d62728"])
    st.caption("Green: Gross Margin | Red: Net Margin. Note the upward trajectory in FY25 due to price optimization.")

with tab2:
    st.subheader("Short-Term Solvency")
    liq_col1, liq_col2 = st.columns([2, 1])
    with liq_col1:
        liq_df = pd.DataFrame({'Metric': ['Current Ratio', 'Quick Ratio'], 'Value': [1.27, 0.90]})
        st.bar_chart(liq_df.set_index('Metric'), color="#ff7f0e")
    with liq_col2:
        st.write("**Analyst Note:**")
        st.write("Edita maintains an efficient cash-conversion cycle. While the Quick Ratio is below 1.0, the high inventory turnover of snacks mitigates liquidity risk.")

with tab3:
    st.subheader("Relative & Fundamental Valuation")
    v_col1, v_col2 = st.columns([2, 1])
    
    # Simple DCF Logic
    shares = 1400027312
    term_value = (df_forecast.iloc[-1]['Revenue'] * 0.12) / (wacc - 0.03)
    dcf_price = (term_value * 1e9 / shares)
    
    with v_col1:
        val_df = pd.DataFrame({
            'Method': ['Market Price', 'Sector Avg (PE)', 'DCF Estimate', 'Premium Target'],
            'Price': [30.49, 33.50, dcf_price, 38.89]
        })
        st.bar_chart(val_df.set_index('Method'), color="#9467bd")
        
    with v_col2:
        st.metric("DCF Intrinsic Value", f"{dcf_price:.2f} EGP")
        upside = ((dcf_price/30.49)-1)*100
        st.write(f"**Implied Upside:** {upside:+.1f}%")
        if upside > 0:
            st.success("Rating: BUY")
        else:
            st.error("Rating: OVERVALUED")

# --- PROFESSIONAL FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by <b>Abdelrahim Elsweedy</b> | FMVA | Certified Data Analayst
    </div>
    """, unsafe_allow_html=True)
