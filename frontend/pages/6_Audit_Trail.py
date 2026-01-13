import streamlit as st
import pandas as pd
from utils import get_data, load_css

load_css()

st.title("🛡️ Audit Trail System")

st.markdown("### Immutable Log of Actions")

logs = get_data("/admin/audit-log")

if logs:
    df = pd.DataFrame(logs)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No audit logs found.")
