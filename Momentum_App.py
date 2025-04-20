import streamlit as st
import pandas as pd
# import altair as alt

from interface.momentum import MomentumApp

st.title("📈 股票动量策略分析工具")
st.markdown("本工具适配格式：包括多支股票的 `日期`、`收盘价`、`股票代码` 列，自动筛选近60日涨幅最强股票进行动量模拟。")

# 上传文件
uploaded_file = st.file_uploader("上传你的CSV文件（包含'日期'、'收盘价'、'股票代码'列）", type=['csv'])

# if uploaded_file:
#     df = pd.read_csv(uploaded_file, dtype={'股票代码': str})
#     df = df.reset_index(drop=True)
#     df['日期'] = pd.to_datetime(df['日期'])
#     # df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
#     # df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

#     df = df.sort_values(['股票代码', '日期'])

#     N = st.slider("📅 选择动量观察窗口（天）", min_value=5, max_value=90, value=30, step=1)

#     # 动量排名数量 slider
#     top_k = st.slider("🏆 选择展示动量排名前几的股票", min_value=10, max_value=300, value=100, step=10)
    
#     # 对每只股票分别计算 N 日动量
#     df['动量基准价'] = df.groupby('股票代码')['收盘价'].shift(N)
#     df['动量'] = (df['收盘价'] - df['动量基准价']) / df['动量基准价']

#     # 提取最新日期每只股票的动量
#     latest_date = df['日期'].max()
#     latest_df = df[df['日期'] == latest_date][['股票代码', '动量']].dropna()

#     # 显示前100个动量排名
#     top_k = 100  # 固定为前100
#     top_momentum = latest_df.sort_values('动量', ascending=False).head(top_k)

#     st.subheader(f"📊 最近日期：{latest_date.date()}，动量排名前 {top_k} 的股票")
#     top_momentum = top_momentum.reset_index(drop=True)
#     st.dataframe(top_momentum)

#     # # 可视化
#     # # st.bar_chart(top_momentum.sort_values('动量', ascending=False).set_index('股票代码')['动量'])
#     # top_momentum_sorted = top_momentum.sort_values('动量', ascending=False)
#     # st.bar_chart(top_momentum_sorted.set_index('股票代码')['动量'])

    
#     # 使用 Altair 绘制柱状图，按动量值降序排列
#     chart = alt.Chart(top_momentum).mark_bar().encode(
#         x=alt.X('股票代码:N', title='股票代码'),
#         y=alt.Y('动量:Q', title='动量'),
#         color='动量:Q',
#         tooltip=['股票代码', '动量']
#     ).properties(
#         width=800,
#         height=400
#     ).configure_axis(
#         labelAngle=45  # 如果标签过长，可以调整角度
#     )

#     # 显示 Altair 图表
#     st.altair_chart(chart, use_container_width=True)


#     st.markdown("---")
#     st.markdown("🧠 策略说明：")
#     st.markdown(f"""
#     - 选股逻辑：选取最近 **{N} 天内涨幅最高** 的前 **{top_k}** 支股票。
#     - 仿真方法：等权重买入这些股票，计算组合的净值随时间的变化。
#     - 应用提示：可尝试不同时间窗口 & 股票数，优化策略参数。
#     """)














if uploaded_file:
    df = pd.read_csv(uploaded_file, dtype={'股票代码': str})
    df = df.reset_index(drop=True)
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values(['股票代码', '日期'])
    N = st.slider("📅 选择动量观察窗口（天）", min_value=5, max_value=90, value=30, step=1)
    st.markdown("---")
    st.markdown("🧠 策略说明：")
    st.markdown(f"""
    - 选股逻辑：选取最近 **{N} 天内涨幅最高** 的前 **{top_k}** 支股票。
    - 仿真方法：等权重买入这些股票，计算组合的净值随时间的变化。
    - 应用提示：可尝试不同时间窗口 & 股票数，优化策略参数。
    """)

    # 动量排名数量 slider
    top_k = st.slider("🏆 选择展示动量排名前几的股票", min_value=10, max_value=300, value=100, step=10)
    st.subheader(f"📊 最近日期：{latest_date.date()}，动量排名前 {top_k} 的股票")
    st.dataframe(top_momentum)

    m = MomentumApp(df)
    m.get_top_momentum(N, top_k)
    chart = m.get_bar_chart(width=800, height=400, labelAngle=45)
  
    # 显示 Altair 图表
    st.altair_chart(chart, use_container_width=True)
