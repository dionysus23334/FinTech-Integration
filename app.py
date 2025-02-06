import streamlit as st
from components.chatbots import load_chatbot

pages_manager = st.navigation(
    [
        st.Page("Home.py"),
        st.Page("Chatbot.py"),
        st.Page("Word_Cloud.py")
        ]
    )

with st.sidebar:
    load_chatbot()

pages_manager.run()
