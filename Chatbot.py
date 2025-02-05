import streamlit as st

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store messages as a list of dictionaries

from components.chatbots import Chatbot_GLM4

api_key = "6dd4521590f14ea33d8288e5037c6215.aDsJWqIDbkt1Al8y"  # 请填写您自己的APIKey

chatbot_glm=Chatbot_GLM4(api_key)

# Main Chat Interface
st.title("Simple Chat Interface")

st.header("Chat History")
messages = st.container()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages from the session state
with messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Input box for new messages
if prompt := st.chat_input("Say something"):
    # Save user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "user", "history_content": prompt})
    # Display the user message
    with messages:
        with st.chat_message("user"):
            st.write(prompt)

    # Generate and save assistant's response
    response = chatbot_glm.answer(f"user: {prompt}" + f"(history: {st.session_state.chat_history})")
    st.session_state.messages.append({"role": "ai", "content": response})
    st.session_state.chat_history.append({"role": "ai", "history_content": response})
    # Display the assistant's response
    with messages:
        with st.chat_message("ai"):
            st.write(response)
        with st.chat_message("assistant"):
            st.write(st.session_state.chat_history)

