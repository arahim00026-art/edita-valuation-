import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Edita Valuation Dashboard", layout="wide")

st.title("🍰 Edita Food Industries Valuation Dashboard")
st.sidebar.header("Economic Assumptions")

# Inputs
rev_growth = st.sidebar.slider("Annual Revenue Growth (%)", 0.05, 0.40, 0.20)
wacc = st.sidebar.slider("WACC / Discount Rate (%)", 0.10, 0.25, 0.18)

# Core Data
df = pd.DataFrame({
    'Year': [2024, 2025],
    'Revenue': [16.15, 20.92],
    'Net_Profit': [1.61, 2.70]
})

# Projections
current_rev = 20.92
forecast = []
for year in [2026, 2027, 2028, 2029, 2030]:
    current_rev *= (1 + rev_growth)
    forecast.append({'Year': year, 'Revenue': current_rev, 'Net_Profit': current_rev * 0.12})

full_df = pd.concat([df, pd.DataFrame(forecast)])

# Layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("Projected Revenue (Billions EGP)")
    st.line_chart(full_df.set_index('Year')['Revenue'])

with col2:
    st.subheader("Valuation Summary")
    terminal_val = (forecast[-1]['Revenue'] * 0.12) / (wacc - 0.03)
    st.metric("Terminal Value Estimate", f"{terminal_val:.2f}B EGP")
    st.write("This interactive model allows you to simulate how Edita's valuation shifts based on inflation and interest rate hikes.")
