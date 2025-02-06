from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from data_collection.spider import SimpleSpider
from data_collection.extract_info import extract_main_info
import pandas as pd
from zhipuai import ZhipuAI

link = st.text_input("输入网站链接（URL）",value="https://www.cls.cn/")

def analyze_sentiments(events):
    api_key = "6dd4521590f14ea33d8288e5037c6215.aDsJWqIDbkt1Al8y"  # 请填写您自己的APIKey
    client = ZhipuAI(api_key=api_key)  # 请用你的API Key替换这里
    
    # 准备批量情感分析请求
    prompt = f'''
    根据下面这段话：
    {events}
    返回它的情感特征，如
    Positive返回1
    Negative返回-1
    Neutral返回0
    不要返回其他内容只在-1，0，1之间选择
    如一共有5句话
    [...,...,...,...,...]
    
    返回格式：
    [0,-1,1,0,-1]
    '''

    # 创建聊天完成请求
    response = client.chat.completions.create(
        model="glm-4",  # 使用的模型
        messages={"role": "user", "content": prompt},
    )
    
    # 从响应中获取回答内容
    sentiments = response.choices[0].message.content
    return sentiments

def generate_word_cloud(text_input):
    # 创建词云对象
    wordcloud = WordCloud(
        font_path="./fonts/SimHei.ttf",
        width=800, height=600,
        background_color='white'
    ).generate(text_input)

    # 显示词云图片
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    return plt

simplespider = SimpleSpider()
data_example = simplespider.scrape_website(link)

plot = generate_word_cloud(data_example['text'])
plot.show()
st.pyplot(plot)

sentiment_dict = {
    '1':'Positive',
    '0':'Neutral',
    '-1':'Negative'
}

if text_input := data_example['text']:
    # Step 1: 提取主体信息
    events = extract_main_info(text_input)
    st.write(events)
    
    # Step 2: 对每个事件进行情绪分析
    sentiments = analyze_sentiments(events)
    st.write(sentiments)
    
    data = [{"简化内容": event, "情绪": sentiment_dict[sentiment]} for event, sentiment in zip(events, sentiments)]

    # 转换为 DataFrame 并展示
    df = pd.DataFrame(data)
    st.dataframe(df)

st.write(data_example['links'])
