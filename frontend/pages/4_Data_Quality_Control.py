import streamlit as st
from utils import get_data, load_css

load_css()

st.title("✅ Data Quality Control")

st.markdown("### Integrity Checks & Validations")

controls = get_data("/reports/controls")

if controls:
    status = controls.get("status", "GREEN")
    color = "green" if status == "GREEN" else "orange" if status == "YELLOW" else "red"
    
    st.subheader(f"Overall Status: :{color}[{status}]")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Negative Incurred", controls.get("negative_incurred"))
    c2.metric("Missing Segment", controls.get("missing_segment"))
    c3.metric("Future Dates", controls.get("future_dates"))
    
    if status != "GREEN":
        st.error("Critical data quality issues detected. Please review the raw data inputs.")
    else:
        st.success("All systems operational. Data quality is within acceptable limits.")
else:
    st.error("Could not load control status.")
