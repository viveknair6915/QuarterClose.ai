import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data, load_css

load_css()

st.title("💰 Cashflow & GLT Analysis")

year = st.sidebar.number_input("Year", 2020, 2030, 2024)

data = get_data(f"/reports/cashflow/{year}")

if data:
    df = pd.DataFrame(data)
    
    st.subheader("Monthly Net Cash Position")
    
    # Color logic for bars
    df['color'] = df['net_cashflow'].apply(lambda x: 'green' if x >= 0 else 'red')
    
    fig = px.bar(df, x='month', y='net_cashflow', color='color', title="Net Cashflow by Month", color_discrete_map="identity")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Flows")
    st.dataframe(df[['month', 'inflow', 'outflow', 'net_cashflow', 'status']], use_container_width=True)
else:
    st.info("No cashflow data available.")
