import streamlit as st
import pandas as pd
from data_collection.spider import AutoSpider

spider = AutoSpider()
df = spider.get_dataframe()

# 页面标题
st.title("股票详情数据展示")

# 展示表格（可交互）
st.dataframe(df)

# 也可以选择 st.table(df) 显示为静态表格
# st.table(df)

