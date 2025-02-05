from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

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

from data_collection.spider import SimpleSpider

simplespider = SimpleSpider()
data_example = simplespider.scrape_website("https://www.cls.cn/")

plot = generate_word_cloud(data_example['text'])
plot.show()
st.pyplot(plot)
