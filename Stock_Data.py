import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("📈 股票数据可视化分析平台")

uploaded_file = st.file_uploader("上传你的CSV文件", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 日期转换
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"])
    else:
        st.error("文件中缺少 '日期' 列")
        st.stop()

    # 股票代码列表
    stock_list = df["股票代码"].unique().tolist()
    selected_stock = st.selectbox("选择一个股票代码", stock_list)

    stock_df = df[df["股票代码"] == selected_stock]

    # 选择图表类型
    chart_type = st.selectbox("选择图表类型", ["折线图（多指标）", "柱状图（成交额）", "饼图（某日成交量占比）"])

    if chart_type == "折线图（多指标）":
        available_metrics = [col for col in stock_df.columns if col not in ["日期", "股票代码"]]
        selected_metrics = st.multiselect("选择要绘制的指标", available_metrics)

        fig = go.Figure()
        yaxis_count = 1
        layout_yaxes = {}

        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#d62728"]

        for i, metric in enumerate(selected_metrics):
            yaxis_name = "yaxis" if yaxis_count == 1 else f"yaxis{yaxis_count}"
            yref = "y" if yaxis_count == 1 else f"y{yaxis_count}"

            fig.add_trace(go.Scatter(
                x=stock_df["日期"],
                y=stock_df[metric],
                mode="lines+markers",
                name=metric,
                yaxis=yref,
                line=dict(color=colors[i % len(colors)])
            ))

            layout_yaxes[yaxis_name] = dict(
                title=metric,
                overlaying="y" if yaxis_count > 1 else None,
                side="right" if yaxis_count % 2 == 0 else "left",
                position=1.0 - 0.05 * (yaxis_count - 1) if yaxis_count > 1 else None
            )

            yaxis_count += 1

        fig.update_layout(
            title=f"{selected_stock} 指标趋势图",
            xaxis=dict(title="日期"),
            height=600,
            width=1000,
            **layout_yaxes
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "柱状图（成交额）":
        if "成交额" in stock_df.columns:
            fig = go.Figure(go.Bar(
                x=stock_df["日期"],
                y=stock_df["成交额"],
                marker_color='lightskyblue',
                name="成交额"
            ))
            fig.update_layout(title=f"{selected_stock} 每日成交额柱状图", xaxis_title="日期", yaxis_title="成交额")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("该数据中不包含 '成交额' 字段")

#     elif chart_type == "饼图（某日成交量占比）":
#         date_option = st.selectbox("选择某一天", stock_df["日期"].dt.date.unique())
#         filtered_df = df[df["日期"].dt.date == date_option]
#         if "成交量" in filtered_df.columns:
#             fig = go.Figure(go.Pie(
#                 labels=filtered_df["股票代码"],
#                 values=filtered_df["成交量"],
#                 textinfo="percent+label"
#             ))
#             fig.update_layout(title=f"{date_option} 成交量占比图")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("该数据中不包含 '成交量' 字段")
