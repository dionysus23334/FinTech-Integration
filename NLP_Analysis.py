
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from data_collection.spider import SimpleSpider
from data_collection.extract_info import extract_main_info
from zhipuai import ZhipuAI
import json

# 获取用户输入的 URL
link = st.text_input("输入网站链接（URL）", value="https://www.cls.cn/")

API_KEY = "6dd4521590f14ea33d8288e5037c6215.aDsJWqIDbkt1Al8y"  # 请填写您自己的APIKey

def batch_analyze_sentiment(events):
    """
    使用一次 API 请求对所有事件进行情感分析，返回一个情感标签列表。
    """
    if not API_KEY:
        st.error("未找到 API Key，请设置环境变量 ZHIPU_API_KEY。")
        return ["Error"] * len(events)

    prompt = f'''
    请对以下文本列表进行情感分析，并返回一个 JSON 格式的列表：
    - Positive 返回 1
    - Neutral 返回 0
    - Negative 返回 -1
    
    例如：
    输入：
    ["事件1", "事件2", "事件3"]
    
    输出：
    {{"results": [1, 0, -1]}}

    请严格按照 JSON 格式返回，不要包含额外信息：
    {json.dumps(events, ensure_ascii=False)}
    '''

    client = ZhipuAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": prompt}]
        )
        sentiment_response = response.choices[0].message.content.strip()

        # 解析返回的 JSON
        sentiment_data = json.loads(sentiment_response)

        if "results" in sentiment_data and isinstance(sentiment_data["results"], list):
            return sentiment_data["results"]
        else:
            return ["Error"] * len(events)

    except Exception as e:
        st.error(f"API 调用失败: {e}")
        return ["Error"] * len(events)

def generate_word_cloud(text_input):
    """
    生成词云
    """
    try:
        wordcloud = WordCloud(
            font_path = "./fonts/SimHei.ttf",  # Windows 可能需要具体路径
            width = 800, height= 600,
            background_color='white'
        ).generate(text_input)

        plt.figure(figsize=(8, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        return plt
    except Exception as e:
        st.error(f"词云生成失败: {e}")
        return None

# 爬取网页内容
spider = SimpleSpider()
data_example = spider.scrape_website(link)

if 'text' in data_example and data_example['text']:
    text_content = data_example['text']

    # 显示词云
    plot = generate_word_cloud(text_content)
    if plot:
        st.pyplot(plot)

    sentiment_dict = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}

    # 提取主要信息
    events = extract_main_info(text_content)

    # 进行批量情感分析
    sentiment_results = batch_analyze_sentiment(events)

    # 组装结果
    data = []
    for event, sentiment in zip(events, sentiment_results):
        sentiment_label = sentiment_dict.get(sentiment, "Error")
        data.append({"简化内容": event, "情绪": sentiment_label})

    # 展示情感分析结果
    df = pd.DataFrame(data)
    st.dataframe(df)
else:
    st.warning("未能从该网站提取有效文本，请检查 URL 或网站结构。")
