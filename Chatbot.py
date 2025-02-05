import streamlit as st

# Sidebar Chat Messages
with st.sidebar:
    st.header("Chat History")
    messages = st.container(height=300)
    # Assigning a unique key for the sidebar chat input
    if prompt := st.chat_input("Say something", key="sidebar_input"):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")

# Main Chat Interface
st.title("Simple Chat Interface")

# Display Initial AI and User Messages
with st.chat_message("ai"):
    st.write("Hello 👋")

with st.chat_message("user"):
    st.write("Hello 👋")

# Chat Input Area with a unique key
user_input = st.chat_input("Say something", key="main_input")

# Send Button Logic
def send_message():
    if user_input:
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(f"Echo: {user_input}")

# Send Button
st.button("Send", on_click=send_message)
