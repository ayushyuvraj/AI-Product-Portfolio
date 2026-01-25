import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# --- PRODUCT CONFIGURATION (The "Why") ---
# Setting the page layout to 'Wide' to resemble a real Monitoring Dashboard
st.set_page_config(page_title="Fraud Command Center", layout="wide", page_icon="🛡️")

# --- SIDEBAR: STRATEGY CONFIGURATION (The "functional" Layer) ---
st.sidebar.header("⚙️ Risk Policy Configurator")
st.sidebar.markdown("Define the 'Dynamic Friction' logic below. Changes deploy in real-time.")

# 1. The Rule Builder
st.sidebar.subheader("1. Velocity & Value Rules")
max_amount = st.sidebar.slider("🚨 High Value Threshold (₹)", 10000, 200000, 50000, step=5000, help="Transactions above this amount trigger enhanced scrutiny.")
location_check = st.sidebar.checkbox("🌍 Enforce Geo-Fencing", value=True, help="Flag transactions from high-risk IP addresses.")

# 2. The Dynamic Friction Logic (Green/Yellow/Red Zones)
st.sidebar.subheader("2. Trust Score Thresholds")
st.sidebar.markdown("Set the limits for **Allow**, **Challenge (OTP)**, and **Block**.")
friction_level = st.sidebar.slider(
    "Set Challenge Zone (Yellow)", 
    0, 100, (50, 85), 
    help="Scores below lower limit = Allow. Scores above upper limit = Block. In-between = OTP."
)
green_limit = friction_level[0]
red_limit = friction_level[1]

# --- MAIN DASHBOARD ---
st.title("🛡️ Fraud Command Center (FCC)")
st.markdown(f"""
**Status:** 🟢 System Active | **Architecture:** Hybrid Async (Kafka/Redis) | **Latency SLA:** <200ms
\nThis dashboard allows Risk Analysts to simulate and deploy **Dynamic Friction Strategies** without engineering intervention.
""")

st.divider()

# --- SIMULATION ENGINE (Simulating Kafka Stream) ---
# We generate fake transaction data to simulate live traffic
def generate_data():
    np.random.seed(42) # For consistent demo results
    data = pd.DataFrame({
        'Transaction_ID': [f'TXN-{x}' for x in range(1000, 1500)],
        'Amount': np.random.randint(500, 150000, 500),
        'Trust_Score': np.random.randint(1, 100, 500), # 100 = High Risk
        'Location_Risk': np.random.choice([0, 1], 500, p=[0.9, 0.1]) # 1 = Risky Geo
    })
    return data

raw_data = generate_data()

# --- LOGIC ENGINE (Applying your Rules) ---
# This mimics the Python Rule Engine running on Redis data
def apply_risk_logic(row):
    # Hard Rules (High Value + Risky Location)
    if row['Amount'] > max_amount and location_check and row['Location_Risk'] == 1:
        return "🔴 BLOCK"
    
    # Trust Score Logic (Dynamic Friction)
    if row['Trust_Score'] > red_limit:
        return "🔴 BLOCK"
    elif row['Trust_Score'] > green_limit:
        return "🟡 CHALLENGE (OTP)"
    else:
        return "🟢 ALLOW"

# Apply logic to data
raw_data['Action'] = raw_data.apply(apply_risk_logic, axis=1)

# --- IMPACT SIMULATOR (Shadow Mode) ---
st.subheader("📊 Live Impact Simulator")
c1, c2, c3 = st.columns(3)

# Metrics Calculation
total_txns = len(raw_data)
blocked_txns = raw_data[raw_data['Action'] == "🔴 BLOCK"]
challenge_txns = raw_data[raw_data['Action'] == "🟡 CHALLENGE (OTP)"]
allowed_txns = raw_data[raw_data['Action'] == "🟢 ALLOW"]

blocked_val = blocked_txns['Amount'].sum()
revenue_at_risk = challenge_txns['Amount'].sum()

# Display KPIs
c1.metric("Total Transactions (Last Hour)", f"{total_txns}", delta="5000 TPS Capacity")
c2.metric("Fraud Prevented (Blocked)", f"₹{blocked_val:,}", delta_color="inverse")
c3.metric("Revenue Saved via OTP (Challenge)", f"₹{revenue_at_risk:,}", help="This revenue would have been lost if we used a binary Block model.")

# --- VISUALIZATION ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### Decision Distribution")
    fig_pie = px.pie(raw_data, names='Action', title='Impact of Current Policy', 
                     color='Action',
                     color_discrete_map={'🔴 BLOCK':'red', '🟢 ALLOW':'green', '🟡 CHALLENGE (OTP)':'orange'})
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.markdown("### Risk vs. Value Scatter")
    st.markdown("See where high-value transactions fall on the Trust Score spectrum.")
    fig_scatter = px.scatter(raw_data, x='Trust_Score', y='Amount', color='Action',
                             color_discrete_map={'🔴 BLOCK':'red', '🟢 ALLOW':'green', '🟡 CHALLENGE (OTP)':'orange'},
                             hover_data=['Transaction_ID'])
    # Add vertical lines for thresholds
    fig_scatter.add_vline(x=green_limit, line_dash="dash", line_color="green", annotation_text="Green Zone")
    fig_scatter.add_vline(x=red_limit, line_dash="dash", line_color="red", annotation_text="Red Zone")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- RAW DATA VIEW ---
with st.expander("🔎 View Real-Time Transaction Logs (Simulated Kafka Stream)"):
    st.dataframe(raw_data.sort_values(by='Amount', ascending=False))