import streamlit as st

pages_manager = st.navigation(
    [
        st.Page("Home.py"),
        st.Page("Chatbot.py"),
        st.Page("NLP_Analysis.py"),
        st.Page("Stock_Data.py"),
        st.Page("RPS_And_STD.py"),
        st.Page("Events_And_Prices.py"),
        st.Page("Momentum_App.py"),
        ]
    )

pages_manager.run()
