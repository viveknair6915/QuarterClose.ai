import streamlit as st
import pandas as pd
from utils import get_data, load_css

load_css()

st.title("🚨 Large Loss Reporting")

st.markdown("""
### Significant Claims Monitor
Claims exceeding the threshold (e.g., $100k) are automatically flagged for review.
""")

losses = get_data("/reports/large-loss")

if losses:
    df = pd.DataFrame(losses)
    st.dataframe(df, use_container_width=True)
    
    st.download_button(
        label="Download Report as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='large_losses.csv',
        mime='text/csv'
    )
else:
    st.info("No large losses detected.")
