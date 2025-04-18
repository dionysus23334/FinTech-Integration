import streamlit as st

pages_manager = st.navigation(
    [
        st.Page("Home.py"),
        st.Page("Chatbot.py"),
        st.Page("NLP_Analysis.py"),
        st.Page("Stock_Data.py"),
        st.Page("RPS_and_STD.py"),
        ]
    )

pages_manager.run()
