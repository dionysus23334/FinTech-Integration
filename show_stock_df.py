

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 股票价格趋势可视化")

uploaded_file = st.file_uploader("上传你的CSV文件", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 日期处理
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"])

    # 股票代码列表
    stock_list = df["股票代码"].unique().tolist()
    selected_stock = st.selectbox("选择股票代码", stock_list)

    # 指标选择
    default_metrics = ["收盘价", "涨跌幅", "成交量"]
    available_metrics = [col for col in df.columns if col not in ["日期", "股票代码"]]
    selected_metrics = st.multiselect("选择要显示的指标", available_metrics, default=default_metrics)

    # 过滤数据
    stock_df = df[df["股票代码"] == selected_stock].copy()
    stock_df = stock_df.sort_values("日期")

    # 转换数值列
    for metric in selected_metrics:
        stock_df[metric] = pd.to_numeric(stock_df[metric], errors="coerce")

    # 画图
    fig = go.Figure()
    yaxis_count = 1
    yaxis_config = {}

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#d62728"]

    for i, metric in enumerate(selected_metrics):
        yaxis_name = "y" if yaxis_count == 1 else f"y{yaxis_count}"
        fig.add_trace(go.Scatter(
            x=stock_df["日期"],
            y=stock_df[metric],
            mode="lines+markers",
            name=metric,
            yaxis=yaxis_name,
            line=dict(color=colors[i % len(colors)])
        ))

        # 动态添加 y 轴
        yaxis_config[yaxis_name] = dict(
            title=metric,
            overlaying="y" if yaxis_count > 1 else None,
            side="right" if yaxis_count % 2 == 0 else "left",
            position=1.0 - 0.05 * yaxis_count if yaxis_count > 1 else None,
        )
        yaxis_count += 1

    fig.update_layout(
        title=f"{selected_stock} 指标趋势图",
        xaxis=dict(title="日期"),
        height=600,
        width=1000,
        **yaxis_config
    )

    st.plotly_chart(fig, use_container_width=True)
