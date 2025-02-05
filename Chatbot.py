import streamlit as st

# Main Chat Interface
st.title("Simple Chat Interface")

st.header("Chat History")
messages = st.container()

i=0
while True:
    key=f'{i}'
    # Assigning a unique key for the sidebar chat input
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user",key=key).write(prompt)
        messages.chat_message("assistant",key=key).write(f"Echo: {prompt}")
        i+=1

