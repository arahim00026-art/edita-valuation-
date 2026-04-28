import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Edita Financial Intelligence", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_content_usage=True)

st.title("🍰 Edita Food Industries: Financial Performance & Valuation")
st.markdown("---")

# --- SIDEBAR: DYNAMIC ASSUMPTIONS ---
st.sidebar.header("🕹️ Control Panel")
st.sidebar.markdown("Adjust these to stress-test the valuation.")
rev_growth = st.sidebar.slider("Annual Revenue Growth (%)", 0.05, 0.40, 0.20)
wacc = st.sidebar.slider("WACC (Discount Rate) (%)", 0.10, 0.25, 0.18)

# --- DATA ENGINE ---
# Historicals
df_hist = pd.DataFrame({
    'Year': [2024, 2025],
    'Revenue': [16.15, 20.92],
    'Net_Profit': [1.61, 2.70],
    'Gross_Margin': [30.4, 33.9]
})

# Projections
current_rev = 20.92
forecast = []
for year in [2026, 2027, 2028, 2029, 2030]:
    current_rev *= (1 + rev_growth)
    forecast.append({'Year': year, 'Revenue': current_rev, 'Net_Profit': current_rev * 0.12})
df_full = pd.concat([df_hist, pd.DataFrame(forecast)])

# --- TOP ROW: KPI METRICS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("FY25 Revenue", "20.9B EGP", "+29.5%")
col_m2.metric("Net Profit Margin", "11.7%", "+2.9%")
col_m3.metric("ROE", "39.9%", "Premium")
col_m4.metric("Current Ratio", "1.27x", "Healthy")

# --- TABBED ANALYSIS ---
tab1, tab2, tab3 = st.tabs(["📈 Growth & Profitability", "💧 Liquidity & Risk", "💎 Valuation Model"])

with tab1:
    st.subheader("Profitability Expansion")
    c1, c2 = st.columns(2)
    with c1:
        st.write("Revenue Trajectory")
        st.area_chart(df_full.set_index('Year')['Revenue'], color="#1f77b4")
    with c2:
        st.write("Margin Trends (%)")
        # Reuse your margins logic here
        st.line_chart(df_hist.set_index('Year')['Gross_Margin'], color="#2ca02c")

with tab2:
    st.subheader("Liquidity Profile")
    # Visualization for Current/Quick Ratios
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        st.write("Current vs Quick Ratio")
        liq_df = pd.DataFrame({'Metric': ['Current', 'Quick'], 'Value': [1.27, 0.90]})
        st.bar_chart(liq_df.set_index('Metric'))
    with l_col2:
        st.info("The Quick Ratio of 0.90x suggests a lean inventory management strategy, typical for high-turnover FMCG leaders in Egypt.")

with tab3:
    st.subheader("Valuation Framework")
    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        # DCF Calculation
        terminal_val = (forecast[-1]['Revenue'] * 0.12) / (wacc - 0.03)
        shares = 1400027312
        fair_value_share = (terminal_val * 1e9 / shares)
        
        st.write("Football Field: Valuation Ranges")
        valuation_data = {
            'Method': ['DCF Estimate', 'Market Median (PE)', 'Premium Target (PE)', 'Current Price'],
            'Price': [fair_value_share, 34.50, 38.89, 30.49]
        }
        st.bar_chart(pd.DataFrame(valuation_data).set_index('Method'))
    
    with v_col2:
        st.success(f"**DCF Fair Value:** {fair_value_share:.2f} EGP")
        st.write(f"**Upside/Downside:** {((fair_value_share/30.49)-1)*100:.1f}%")
        st.markdown("---")
        st.warning("Valuation is highly sensitive to WACC and Terminal Growth.")

st.markdown("---")
st.caption("Data Source: Edita FY2025 Consolidated Financial Statements | Model by [Your Name]")
