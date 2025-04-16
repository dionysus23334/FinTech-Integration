import streamlit as st
import pandas as pd


df = pd.read_csv("stock_details_data.csv")

# 页面标题
st.title("股票详情数据展示")

# 展示表格（可交互）
st.dataframe(df)

# 也可以选择 st.table(df) 显示为静态表格
# st.table(df)

