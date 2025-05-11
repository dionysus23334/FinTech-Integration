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
        st.Page("Average_Lines.py"),
        st.Page("Get_Stocks_Pool.py"),
        st.Page("Market_Values.py"),
        st.Page("Traditional_Method.py"),
        st.Page("Machine_Learning.py"),
        st.Page("Money_Flow.py"),
        st.Page("KDJ_Analysis.py"),
    ]
    )

pages_manager.run()
