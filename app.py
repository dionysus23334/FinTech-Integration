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
        st.Page("Calculate_AvgLines.py"),
        st.Page("Average_Lines.py")
        ]
    )

pages_manager.run()
