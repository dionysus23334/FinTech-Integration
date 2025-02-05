import streamlit as st
import numpy as np

# Insert a chat message container.
with st.chat_message("ai"):
    st.write("Hello 👋")

with st.chat_message("user"):
    st.write("Hello 👋")

# Display a chat input widget inline.
with st.container():
    st.chat_input("Say something")
import streamlit as st

with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")

# 发送按钮
st.button("发送", on_click=send_message)
