import streamlit as st
import pandas as pd
from utils import load_data, helpers
from utils.constants import *

def show() -> None:
    helpers.render_page_header("💡 Business Insights", "Key business metrics and project summary.")
    
    insights_df = load_data.load_business_insights()
    project_df = load_data.load_project_summary()
    
    if insights_df.empty and project_df.empty:
        st.warning("No insights data available.")
        return
        
    st.markdown("### Key Business Metrics")
    if not insights_df.empty:
        metrics = insights_df.to_dict('records')
        
        cols = st.columns(4)
        for i, row in enumerate(metrics):
            with cols[i % 4]:
                st.metric(row['Metric'], row['Value'])
                
        st.markdown("### Insights Data")
        st.dataframe(insights_df, use_container_width=True)
        
        csv_insights = insights_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Insights Data",
            data=csv_insights,
            file_name='business_insights.csv',
            mime='text/csv',
            key='dl_insights'
        )
                
    st.markdown("### Project Summary")
    if not project_df.empty:
        proj_metrics = project_df.to_dict('records')
        for row in proj_metrics:
            st.info(f"**{row['Project Metric']}**: {row['Value']}")
            
    st.markdown("### Executive Summary")
    st.success("Business insights provide a high-level overview of the company's health and project status.")
    
    helpers.render_footer("Business Insights")
