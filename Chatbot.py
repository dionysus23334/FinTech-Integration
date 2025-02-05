import streamlit as st

# Main Chat Interface
st.title("Simple Chat Interface")

st.header("Chat History")
messages = st.container(height=300)
# Assigning a unique key for the sidebar chat input
if prompt := st.chat_input("Say something", key="sidebar_input"):
    messages.chat_message("user").write(prompt)
    messages.chat_message("assistant").write(f"Echo: {prompt}")
