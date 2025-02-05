import streamlit as st

pages_manager = st.navigation(
    [
        st.Page("Home.py"),
        st.Page("SearchWeb.py"),
        st.Page("plot_df.py"),
        st.Page("plot_demo.py"),
        st.Page("Word_Cloud.py")
        ]
    )

pages_manager.run()
