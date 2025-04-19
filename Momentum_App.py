import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="动量策略分析", layout="wide")

st.title("📈 股票动量策略分析工具")
st.markdown("本工具适配格式：包括多支股票的 `日期`、`收盘价`、`股票代码` 列，自动筛选近60日涨幅最强股票进行动量模拟。")

# 上传文件
uploaded_file = st.file_uploader("请上传包含多个股票的CSV文件", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['日期'])
    st.success("✅ 数据加载成功！")

    # 显示原始数据样例
    with st.expander("点击展开查看部分原始数据"):
        st.dataframe(df.head(10))

    # 只保留需要的列
    df = df[['日期', '股票代码', '收盘价']]

    # 透视表：宽格式，行是日期，列是股票代码，值是收盘价
    price_df = df.pivot(index='日期', columns='股票代码', values='收盘价').sort_index()

    st.subheader("📊 数据概览（收盘价矩阵）")
    st.dataframe(price_df.tail(10))

    # 策略参数
    lookback = st.slider("动量观察期（最近几天涨幅）", min_value=20, max_value=90, value=60)
    top_n = st.slider("选择涨幅排名前 N 的股票", min_value=1, max_value=50, value=10)

    # 计算动量（过去lookback天的涨幅）
    momentum = price_df.pct_change(periods=lookback).iloc[-1]
    selected = momentum.dropna().sort_values(ascending=False).head(top_n).index.tolist()

    st.subheader(f"🚀 当前动量Top{top_n}（观察期{lookback}天）")
    st.dataframe(momentum[selected].sort_values(ascending=False).to_frame(name="涨幅"))

    # 模拟从选中股票中等权买入后的收益情况
    returns = price_df[selected].pct_change().dropna()
    portfolio = (1 + returns).cumprod()

    st.subheader("📈 动量策略组合净值走势")
    st.line_chart(portfolio.mean(axis=1))

    st.markdown("---")
    st.markdown("🧠 策略说明：")
    st.markdown(f"""
    - 选股逻辑：选取最近 **{lookback} 天内涨幅最高** 的前 **{top_n}** 支股票。
    - 仿真方法：等权重买入这些股票，计算组合的净值随时间的变化。
    - 应用提示：可尝试不同时间窗口 & 股票数，优化策略参数。
    """)

else:
    st.info("请上传包含多个股票历史的CSV文件。")

