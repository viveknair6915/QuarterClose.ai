import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_data

st.title("🔮 Predictive Loss Forecasting")

st.markdown("""
### AI-Driven Projections
Using historical claim development patterns to forecast next quarter's liability.
""")

year = st.sidebar.number_input("Base Year", 2020, 2030, 2024)

from utils import get_data, load_css

load_css()

forecast = get_data(f"/reports/forecast/{year}")

if forecast and "projection" in forecast:
    # Top Level Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Projected Liability (Next Q)", f"${forecast['projection']:,.0f}", 
              delta="Trending UP" if forecast['trend_direction'] == "UP" else "Trending DOWN",
              delta_color="inverse")
    c2.metric("Model Confidence", forecast['confidence'], "High")
    c3.metric("Trend Direction", forecast['trend_direction'])
    
    # Visualization
    hist_df = pd.DataFrame(forecast['historical_data'])
    
    fig = go.Figure()
    
    # Historical Line
    fig.add_trace(go.Scatter(
        x=hist_df['month'], 
        y=hist_df['amount'],
        mode='lines+markers',
        name='Historical Actuals',
        line=dict(color='#00CC96', width=3)
    ))
    
    # Projection Point
    next_month = hist_df['month'].max() + 1
    fig.add_trace(go.Scatter(
        x=[next_month],
        y=[forecast['projection']],
        mode='markers',
        name='Forecast',
        marker=dict(color='#AB63FA', size=15, symbol='star')
    ))
    
    fig.update_layout(
        title="Loss Development Trajectory",
        xaxis_title="Month",
        yaxis_title="Incurred Amount ($)",
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("Insufficient data to generate forecast. Please upload claim data first.")
