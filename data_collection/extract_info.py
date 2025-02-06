
from zhipuai import ZhipuAI

# 提取主体信息的提示词模板
def extract_main_info(text):
    api_key = "6dd4521590f14ea33d8288e5037c6215.aDsJWqIDbkt1Al8y"  # 请填写您自己的APIKey
    prompt = f'''
    请严格按返回格式生成回复，不要返回其他脱离格式的信息，否则会对后续文本处理造成干扰和噪音。
    从以下文本中提取出主要的事件信息，并将其表达为多句完整的话，每句话都能完整表达一个事件：
    "{text}"
    返回格式：
    1. 事件1
    2. 事件2
    3. 事件3
    '''
    client = ZhipuAI(api_key=api_key)  # 请用你的API Key替换这里
    # 创建聊天完成请求
    response = client.chat.completions.create(
        model="glm-4",  # 使用的模型
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    # 从响应中获取回答内容
    response_text = response.choices[0].message.content
    # 解析 API 返回结果
    extracted_text = response_text.strip()
    events = [line.strip() for line in extracted_text.split("\n") if line.strip()]
    print(events)
    return events


