import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data

st.title("🌍 Geospatial Risk Map")

st.markdown("### Global Distribution of Claims")

from utils import get_data, load_css

load_css()

geo_data = get_data("/reports/geo-data")

if geo_data:
    df = pd.DataFrame(geo_data)
    df.columns = ['claim_id', 'lat', 'lon', 'amount']
    
    # Interactive Map
    fig = px.scatter_mapbox(
        df, 
        lat="lat", 
        lon="lon", 
        size="amount",
        color="amount",
        hover_name="claim_id",
        zoom=1,
        height=600,
        color_continuous_scale=px.colors.cyclical.IceFire
    )
    
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.head(10), use_container_width=True)
else:
    st.info("No geospatial data available. Upload a dataset with location tags.")
