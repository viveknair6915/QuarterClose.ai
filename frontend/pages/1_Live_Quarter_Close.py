import streamlit as st
import pandas as pd
from utils import post_data, get_data, load_css

load_css()

st.title("🔐 Live Quarter Close Engine")

st.markdown("""
### Quarter Close Control Center
Upload claims data for the current period and lock the quarter once reconciled.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Select Period")
    year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
    quarter = st.selectbox("Quarter", [1, 2, 3, 4])

with col2:
    st.subheader("2. Upload Data")
    uploaded_file = st.file_uploader("Upload Claims Data (CSV/Excel)", type=['csv', 'xlsx'])
    if st.button("Ingest Data"):
        if uploaded_file is not None:
            files = {"file": uploaded_file}
            params = {"year": year, "quarter": quarter}
            res = post_data("/data/upload/claims", files=files, params=params)
            
            if res and "error" in res:
                if "Quarter is closed" in res["error"]:
                    st.warning(f"🔒 **Action Blocked**: Quarter {year} Q{quarter} is already closed. Please select an open period or contact Admin.")
                else:
                    st.error(f"Upload Failed: {res['error']}")
            elif res:
                st.success(f"Successfully processed {res.get('processed')} records.")

st.divider()

st.subheader("3. Close & Lock Period")
st.warning("⚠️ Warning: Closing the quarter is irreversible. No further edits will be allowed.")

if st.button("CONFIRM CLOSE QUARTER"):
    res = post_data("/admin/close-period", params={"year": year, "quarter": quarter})
    if res:
        st.success(f"Period {res.get('period')} is now CLOSED.")
    else:
        st.error("Failed to close period. It might already be closed.")
