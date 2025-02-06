


# 提取主体信息的提示词模板
def extract_main_info(text):
    prompt = f'''
    从以下文本中提取出主要的事件信息，并将其简化为几句话，每句话都能完整表达一个事件：
    "{text}"
    返回格式：
    1. 事件1
    2. 事件2
    3. 事件3
    '''
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    # 解析 API 返回结果
    extracted_text = response.choices[0].text.strip()
    events = [line.strip() for line in extracted_text.split("\n") if line.strip()]
    return events


