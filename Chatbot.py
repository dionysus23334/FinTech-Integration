import streamlit as st

# Main Chat Interface
st.title("Simple Chat Interface")

st.header("Chat History")
messages = st.container()

i=0
while True:
    key=f'{i}'
    # Assigning a unique key for the sidebar chat input
    if prompt := st.chat_input("Say something", key=key):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")
        i+=1

