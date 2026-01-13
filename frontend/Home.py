import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="QuarterClose.ai",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔥 QuarterClose.ai")
st.markdown("### Automated Actuarial Reporting & Control Platform")

from utils import load_css

# Load CSS
load_css()

st.markdown("""
**Welcome to the QuarterClose.ai workspace.** 

This platform is designed to replace manual Excel-based quarter close processes with a robust, auditable, and automated system.

### 🚀 Core Modules:
- **Live Quarter Close**: Manage periodic closing and locking of data.
- **Large Loss Reporting**: Auto-detect and report significant claims.
- **Actual vs Expected**: Monitor deviations from actuarial assumptions.
- **Data Quality**: Automated health checks on input data.
- **Cashflow Analysis**: Liquidity planning and monitoring.
- **Audit Trail**: Full traceability of all actions.

---
*Built for production-grade Actuarial Control.*
""")

# Quick KPI Snapshot (Mock or Real)
col1, col2, col3 = st.columns(3)
col1.metric("Current Period", "2024 Q1", "Open")
col2.metric("Data Quality Score", "98.5%", "+1.2%")
col3.metric("Pending Large Losses", "3", "-1")

st.sidebar.success("Select a module to begin.")
