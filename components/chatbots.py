from zhipuai import ZhipuAI


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

  
