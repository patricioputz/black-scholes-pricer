"""
Black-Scholes Option Pricer - Interactive Web Application
Build by: Patricio Putz
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from black_scholes import BlackScholes

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">📈 Black-Scholes Option Pricer</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Built by Patricio Putz</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">European Options Pricing & Analysis Tool</p>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("⚙️ Option Parameters")

# Input parameters
S = st.sidebar.number_input(
    "Current Stock Price ($)",
    min_value=1.0,
    max_value=10000.0,
    value=100.0,
    step=1.0,
    help="The current market price of the underlying stock"
)

K = st.sidebar.number_input(
    "Strike Price ($)",
    min_value=1.0,
    max_value=10000.0,
    value=100.0,
    step=1.0,
    help="The price at which the option can be exercised"
)

T = st.sidebar.number_input(
    "Time to Maturity (Years)",
    min_value=0.01,
    max_value=10.0,
    value=1.0,
    step=0.01,
    help="Time remaining until option expiration"
)

sigma = st.sidebar.slider(
    "Volatility (σ)",
    min_value=0.01,
    max_value=2.0,
    value=0.20,
    step=0.01,
    help="Annualized standard deviation of stock returns"
)

r = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.1,
    help="Annualized risk-free interest rate"
) / 100  # Convert percentage to decimal

st.sidebar.markdown("---")
st.sidebar.header("💰 P&L Analysis (Optional)")

enable_pnl = st.sidebar.checkbox("Enable P&L Tracking", value=False)

if enable_pnl:
    purchase_price_call = st.sidebar.number_input(
        "Call Purchase Price ($)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=0.1,
        help="Price you paid for the call option"
    )
    
    purchase_price_put = st.sidebar.number_input(
        "Put Purchase Price ($)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=0.1,
        help="Price you paid for the put option"
    )

st.sidebar.markdown("---")
st.sidebar.header("🔥 Heat Map Ranges")

# Heat map range controls in sidebar
vol_min = st.sidebar.number_input(
    "Min Volatility",
    min_value=0.01,
    max_value=2.0,
    value=max(0.05, sigma - 0.3),
    step=0.05,
    help="Minimum volatility for heat map"
)

vol_max = st.sidebar.number_input(
    "Max Volatility",
    min_value=0.01,
    max_value=2.0,
    value=sigma + 0.3,
    step=0.05,
    help="Maximum volatility for heat map"
)

price_min = st.sidebar.number_input(
    "Min Stock Price ($)",
    min_value=1.0,
    max_value=10000.0,
    value=max(1.0, S * 0.7),
    step=5.0,
    help="Minimum stock price for heat map"
)

price_max = st.sidebar.number_input(
    "Max Stock Price ($)",
    min_value=1.0,
    max_value=10000.0,
    value=S * 1.3,
    step=5.0,
    help="Maximum stock price for heat map"
)

    
# Create Black-Scholes object
bs = BlackScholes(S, K, T, r, sigma)

# Calculate prices
call_price = bs.call_price()
put_price = bs.put_price()
    
# Main results section
st.subheader("📊 Option Prices")

col1, col2 = st.columns(2)

with col1:
    call_delta = (call_price - purchase_price_call) if enable_pnl else None

    st.metric(
        label="Call Option Price",
        value=f"${call_price:.2f}",
        delta=round(call_delta, 2) if enable_pnl else None
    )


with col2:
    put_delta = (put_price - purchase_price_put) if enable_pnl else None

    st.metric(
        label="Put Option Price",
        value=f"${put_price:.2f}",
        delta=round(put_delta, 2) if enable_pnl else None
    )

## Greeks section
st.subheader("🔢 The Greeks")

greeks_col1, greeks_col2, greeks_col3, greeks_col4, greeks_col5 = st.columns(5)

with greeks_col1:
    st.metric("Δ Delta (Call)", f"{bs.delta_call():.4f}")
    st.metric("Δ Delta (Put)", f"{bs.delta_put():.4f}")

with greeks_col2:
    st.metric("Γ Gamma", f"{bs.gamma():.6f}")

with greeks_col3:
    st.metric("ν Vega", f"{bs.vega():.2f}")

with greeks_col4:
    st.metric("Θ Theta (Call)", f"{bs.theta_call():.4f}")
    st.metric("Θ Theta (Put)", f"{bs.theta_put():.4f}")

with greeks_col5:
    st.metric("ρ Rho (Call)", f"{bs.rho_call():.2f}")
    st.metric("ρ Rho (Put)", f"{bs.rho_put():.2f}")



# Heat map section
st.subheader("🔥 Sensitivity Analysis - Heat Maps")

st.info(f"📊 Analyzing {vol_max - vol_min:.2f} volatility range and ${price_max - price_min:.0f} price range")

# Generate heat map data
vol_range = np.linspace(vol_min, vol_max, 20)
price_range = np.linspace(price_min, price_max, 20)

call_values = np.zeros((len(vol_range), len(price_range)))
put_values = np.zeros((len(vol_range), len(price_range)))

for i, vol in enumerate(vol_range):
    for j, price in enumerate(price_range):
        bs_temp = BlackScholes(price, K, T, r, vol)
        call_values[i, j] = bs_temp.call_price()
        put_values[i, j] = bs_temp.put_price()

# If P&L tracking is enabled, show P&L instead of raw values
if enable_pnl:
    call_display = call_values - purchase_price_call
    put_display = put_values - purchase_price_put
    colorscale = 'RdYlGn'  # Red for losses, green for profits
    title_suffix = " (P&L)"
else:
    call_display = call_values
    put_display = put_values
    colorscale = 'Blues'
    title_suffix = ""

# Create heat maps
tab1, tab2 = st.tabs(["📞 Call Option", "📉 Put Option"])

with tab1:
    fig_call = go.Figure(data=go.Heatmap(
        z=call_display,
        x=price_range,
        y=vol_range,
        colorscale=colorscale,
        hoverongaps=False,
        hovertemplate='Stock Price: $%{x:.2f}<br>Volatility: %{y:.2f}<br>Value: $%{z:.2f}<extra></extra>'
    ))
    
    fig_call.update_layout(
        title=f'Call Option Values{title_suffix} vs Stock Price & Volatility',
        xaxis_title='Stock Price ($)',
        yaxis_title='Volatility (σ)',
        height=500
    )
    
    st.plotly_chart(fig_call, use_container_width=True)

with tab2:
    fig_put = go.Figure(data=go.Heatmap(
        z=put_display,
        x=price_range,
        y=vol_range,
        colorscale=colorscale,
        hoverongaps=False,
        hovertemplate='Stock Price: $%{x:.2f}<br>Volatility: %{y:.2f}<br>Value: $%{z:.2f}<extra></extra>'
    ))
    
    fig_put.update_layout(
        title=f'Put Option Values{title_suffix} vs Stock Price & Volatility',
        xaxis_title='Stock Price ($)',
        yaxis_title='Volatility (σ)',
        height=500
    )
    
    st.plotly_chart(fig_put, use_container_width=True)

# Payoff diagrams
st.subheader("📈 Payoff Diagrams at Expiration")

# Generate payoff data
stock_prices_payoff = np.linspace(S * 0.5, S * 1.5, 100)
call_payoffs = np.maximum(stock_prices_payoff - K, 0)
put_payoffs = np.maximum(K - stock_prices_payoff, 0)

if enable_pnl:
    call_pnl = call_payoffs - purchase_price_call
    put_pnl = put_payoffs - purchase_price_put

payoff_tab1, payoff_tab2 = st.tabs(["📞 Call Payoff", "📉 Put Payoff"])

with payoff_tab1:
    fig_call_payoff = go.Figure()
    fig_call_payoff.add_trace(go.Scatter(
        x=stock_prices_payoff,
        y=call_payoffs if not enable_pnl else call_pnl,
        mode='lines',
        name='Call ' + ('P&L' if enable_pnl else 'Payoff'),
        line=dict(color='green', width=3)
    ))
    fig_call_payoff.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_call_payoff.add_vline(x=K, line_dash="dash", line_color="red", 
                                annotation_text=f"Strike: ${K}")
    
    fig_call_payoff.update_layout(
        title='Call Option ' + ('P&L' if enable_pnl else 'Payoff') + ' at Expiration',
        xaxis_title='Stock Price at Expiration ($)',
        yaxis_title='P&L ($)' if enable_pnl else 'Payoff ($)',
        height=400
    )
    
    st.plotly_chart(fig_call_payoff, use_container_width=True)

with payoff_tab2:
    fig_put_payoff = go.Figure()
    fig_put_payoff.add_trace(go.Scatter(
        x=stock_prices_payoff,
        y=put_payoffs if not enable_pnl else put_pnl,
        mode='lines',
        name='Put ' + ('P&L' if enable_pnl else 'Payoff'),
        line=dict(color='red', width=3)
    ))
    fig_put_payoff.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_put_payoff.add_vline(x=K, line_dash="dash", line_color="blue",
                                annotation_text=f"Strike: ${K}")
    
    fig_put_payoff.update_layout(
        title='Put Option ' + ('P&L' if enable_pnl else 'Payoff') + ' at Expiration',
        xaxis_title='Stock Price at Expiration ($)',
        yaxis_title='P&L ($)' if enable_pnl else 'Payoff ($)',
        height=400
    )
    
    st.plotly_chart(fig_put_payoff, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>About This Tool</strong></p>
        <p>This Black-Scholes option pricer calculates theoretical prices for European call and put options.</p>
        <p>Built by <strong>Patricio Putz</strong> | <a href="https://www.linkedin.com/in/patricioputz">LinkedIn</a> | <a href="https://github.com/patricioputz">GitHub</a></p>
        <p>Built with Python, Streamlit, NumPy, SciPy, and Plotly</p>
        <p><em>For educational purposes only. Not financial advice.</em></p>
    </div>
""", unsafe_allow_html=True)