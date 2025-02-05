import streamlit as st
import numpy as np

# Insert a chat message container.
with st.chat_message("Agent"):
    st.write("Hello 👋")

with st.chat_message("user"):
    st.write("Hello 👋")

# Display a chat input widget inline.
with st.container():
    st.chat_input("Say something")

