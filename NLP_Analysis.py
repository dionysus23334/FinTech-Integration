from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from data_collection.spider import SimpleSpider
from data_collection.extract_info import extract_main_info
import pandas as pd

link = st.text_input("输入网站链接（URL）",value="https://www.cls.cn/")

def analyze_sentiment(text):
    pass

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

if text_input := data_example['text']:
    # Step 1: 提取主体信息
    events = extract_main_info(text_input)

    # Step 2: 对每个事件进行情绪分析
    data = []
    for event in events:
        sentiment = analyze_sentiment(event)
        data.append({"简化内容": event, "情绪": sentiment})

    # 转换为 DataFrame 并展示
    df = pd.DataFrame(data)
    st.dataframe(df)

