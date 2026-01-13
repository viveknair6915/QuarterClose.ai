import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data, load_css

load_css()

st.title("📉 Actual vs Expected Analysis")

year = st.sidebar.number_input("Analysis Year", 2020, 2030, 2024)

st.subheader(f"AvE Analysis for {year}")

data = get_data(f"/reports/ave/{year}")

if data:
    df = pd.DataFrame(data)
    
    # Metrics
    total_actual = df['actual_loss'].sum()
    total_expected = df['expected_loss'].sum()
    st.metric("Total Variance", f"${total_actual - total_expected:,.0f}", f"{(total_actual/total_expected - 1)*100:.1f}%")

    # Chart
    fig = px.bar(df, x='segment', y=['actual_loss', 'expected_loss'], barmode='group', title="Actual vs Expected by Segment")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
else:
    st.info("No data available for analysis.")
