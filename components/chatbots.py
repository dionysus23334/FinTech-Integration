from zhipuai import ZhipuAI
import streamlit as st

class Chatbot_GLM4:
    def __init__(self, api_key):
        self.api_key = api_key
    def answer(self, inputs):
        """
        使用智谱AI的chat API来回答一个问题。
        参数:
        - question: 字符串，用户的提问。
        返回:
        - response_text: 字符串，智谱AI的回答。
        """
        # 初始化客户端，使用你的API Key
        client = ZhipuAI(api_key=self.api_key)  # 请用你的API Key替换这里
        # 创建聊天完成请求
        response = client.chat.completions.create(
            model="glm-4",  # 使用的模型
            messages=[
                {"role": "user", "content": inputs},
            ],
        )
        # 从响应中获取回答内容
        response_text = response.choices[0].message.content
        return response_text
def load_chatbot():
    # Initialize session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Store messages as a list of dictionaries
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'prompt' not in st.session_state:
        st.session_state.prompt = None
    api_key = "6dd4521590f14ea33d8288e5037c6215.aDsJWqIDbkt1Al8y"  # 请填写您自己的APIKey
    # api_key = st.text_input("输入您的API KEY",value="Your api key")
    chatbot_glm=Chatbot_GLM4(api_key)
    # Main Chat Interface
    st.title("Simple Chat Interface")
    chatbot = st.selectbox(
            'Pick a Chatbot',
            [None, '智谱清言GLM'],args=[1]
        )
    with open('templates/prompt_keep_glm_memory.txt', "r", encoding="utf-8") as file:
        prompt_template = file.read()
    if chatbot == '智谱清言GLM':
        st.header("ChatGLM")
        messages = st.container()
        # Display previous messages from the session state
        with messages:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        if st.session_state.prompt==None:
            st.session_state.prompt=prompt_template
        # Input box for new messages
        if prompt := st.chat_input("Say something"):
            # Save user message to session state
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "user", "history_content": prompt})
            # Display the user message
            with messages:
                with st.chat_message("user"):
                    st.write(prompt)
            _request_ = f"""
    提示词：
    
    {st.session_state.prompt}
    
    此次用户输入：
    
    {prompt}
    
    (对话数据: 
    
    {st.session_state.chat_history}
    
    )
            """
            # Generate and save assistant's response
            response = chatbot_glm.answer(_request_)
            st.session_state.messages.append({"role": "ai", "content": response})
            st.session_state.chat_history.append({"role": "ai", "history_content": response})
            # Display the assistant's response
            with messages:
                with st.chat_message("ai"):
                    st.write(response)
                # with st.chat_message("assistant"):
                #     st.write(st.session_state.chat_history)
    
    if chatbot == None:
        st.header("None")
