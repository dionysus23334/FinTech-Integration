import streamlit as st

pages_manager = st.navigation(
    [
        st.Page("Home.py"),
        st.Page("Chatbot.py"),
        st.Page("Word_Cloud.py")
        ]
    )

pages_manager.run()
