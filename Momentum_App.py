import streamlit as st
import pandas as pd

st.title("📈 动量策略分析 - 长格式数据")

# 上传文件
uploaded_file = st.file_uploader("上传你的CSV文件（包含'日期'、'收盘价'、'股票代码'列）", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df.reset_index(drop=True)
    df['日期'] = pd.to_datetime(df['日期'])
    df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    df = df.sort_values(['股票代码', '日期'])

    N = st.slider("📅 选择动量观察窗口（天）", min_value=5, max_value=90, value=30, step=1)

    # 对每只股票分别计算 N 日动量
    df['动量基准价'] = df.groupby('股票代码')['收盘价'].shift(N)
    df['动量'] = (df['收盘价'] - df['动量基准价']) / df['动量基准价']

    # 提取最新日期每只股票的动量
    latest_date = df['日期'].max()
    latest_df = df[df['日期'] == latest_date][['股票代码', '动量']].dropna()

    # 显示前100个动量排名
    top_k = 100  # 固定为前100
    top_momentum = latest_df.sort_values('动量', ascending=False).head(top_k)

    st.subheader(f"📊 最近日期：{latest_date.date()}，动量排名前 {top_k} 的股票")
    top_momentum = top_momentum.reset_index(drop=True)
    st.dataframe(top_momentum)

    # 可视化
    st.bar_chart(top_momentum.sort_values('动量', ascending=False).set_index('股票代码')['动量'])
