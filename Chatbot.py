import streamlit as st

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store messages as a list of dictionaries

from zhipuai import ZhipuAI

api_key = "9c7fc9a350127ae3"  # 请填写您自己的APIKey

class Chatbot_GLM4:
    def __init__(self):
        self.chat_history=''
    def answer(self,question):
        """
        使用智谱AI的chat API来回答一个问题。

        参数:
        - question: 字符串，用户的提问。

        返回:
        - response_text: 字符串，智谱AI的回答。
        """
        # 初始化客户端，使用你的API Key
        client = ZhipuAI(api_key=api_key)  # 请用你的API Key替换这里
        self.chat_history += question
        # 创建聊天完成请求
        response = client.chat.completions.create(
            model="glm-4",  # 使用的模型
            messages=[
                {"role": "user", "content": self.chat_history},
            ],
        )

        # 从响应中获取回答内容
        response_text = response.choices[0].message.content
        self.chat_history += response_text
        return response_text

chatbot_glm=Chatbot_GLM4()

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
    response = chatbot_glm.answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Display the assistant's response
    with messages:
        with st.chat_message("assistant"):
            st.write(response)
