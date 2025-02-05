import streamlit as st

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store messages as a list of dictionaries

# Main Chat Interface
st.title("Simple Chat Interface")

st.header("Chat History")
messages = st.container()

# Display previous messages from the session state
with messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Input box for new messages
if prompt := st.chat_input("Say something"):
    # Save user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user message
    with messages:
        with st.chat_message("user"):
            st.write(prompt)

    # Generate and save assistant's response
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Display the assistant's response
    with messages:
        with st.chat_message("assistant"):
            st.write(response)
