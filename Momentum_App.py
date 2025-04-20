import streamlit as st
import pandas as pd

from interface.momentum import MomentumApp

st.title("📈 股票动量策略分析工具")
st.markdown("本工具适配格式：包括多支股票的 `日期`、`收盘价`、`股票代码` 列，自动筛选近60日涨幅最强股票进行动量模拟。")

# 上传文件
uploaded_file = st.file_uploader("上传你的CSV文件（包含'日期'、'收盘价'、'股票代码'列）", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file, dtype={'股票代码': str})
    df = df.reset_index(drop=True)
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values(['股票代码', '日期'])
    N = st.slider("📅 选择动量观察窗口（天）", min_value=5, max_value=90, value=30, step=1)
    # 动量排名数量 slider
    top_k = st.slider("🏆 选择展示动量排名前几的股票", min_value=10, max_value=300, value=100, step=10)

    latest_date = df['日期'].max()
    st.subheader(f"📊 最近日期：{latest_date.date()}，动量排名前 {top_k} 的股票")

    m = MomentumApp(df)
    top_momentum = m.get_top_momentum(N, top_k)
    chart = m.get_bar_chart(width=800, height=400, labelAngle=45)
    st.dataframe(top_momentum)

    # 显示 Altair 图表
    st.altair_chart(chart, use_container_width=True)
    
    st.markdown("---")
    st.markdown("🧠 策略说明：")
    st.markdown(f"""
    - 选股逻辑：选取最近 **{N} 天内涨幅最高** 的前 **{top_k}** 支股票。
    - 仿真方法：等权重买入这些股票，计算组合的净值随时间的变化。
    - 应用提示：可尝试不同时间窗口 & 股票数，优化策略参数。
    """)
