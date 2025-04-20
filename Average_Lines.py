import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(page_title="股票均线查看器", layout="wide")
st.title("📈 股票均线可视化工具")

# 上传文件
uploaded_file = st.file_uploader("📤 上传已包含均线数据的CSV文件（需含'日期','股票代码','MA_5','MA_10','MA_20'）", type=["csv"])

if uploaded_file is not None:
    # 读取数据
    df = pd.read_csv(uploaded_file, parse_dates=["日期"], dtype={'股票代码': str})
    # df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    # df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    # 展示全部股票数量
    st.success(f"✅ 数据加载成功，共 {df['股票代码'].nunique()} 支股票")

    # 股票选择
    stock_list = df['股票代码'].unique()
    selected_stock = st.selectbox("📌 请选择股票代码", stock_list)

    # 过滤所选股票
    df_stock = df[df['股票代码'] == selected_stock].sort_values(by="日期")

    # 时间范围选择器
    min_date = df_stock['日期'].min()
    max_date = df_stock['日期'].max()
    start_date, end_date = st.date_input(
        "📅 选择时间范围",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # 过滤所选时间段数据
    mask = (df_stock['日期'] >= pd.to_datetime(start_date)) & (df_stock['日期'] <= pd.to_datetime(end_date))
    df_filtered = df_stock[mask]

    # 折线图展示
    if df_filtered.empty:
        st.warning("⚠️ 当前选择的时间段没有数据，请调整时间范围")
    else:
        st.subheader(f"📊 {selected_stock} 的 {start_date} ~ {end_date} 均线图")
        st.line_chart(
            df_filtered.set_index('日期')[['MA_5', 'MA_10', 'MA_20']],
            use_container_width=True
        )

    # 可选：展开原始数据表格
    with st.expander("📋 查看选中股票的原始数据（当前时间段）"):
        st.dataframe(df_filtered)




    st.title("📉 均线收敛检测器")
    st.markdown("""
    本工具用于检测股票是否处于 **5日、10日、20日均线**的收敛状态。
    
    **收敛定义：**
    - 均线函数差异平方和 $P(t) = (f(t)-g(t))^2 + (g(t)-h(t))^2 + (f(t)-h(t))^2$
    - 若 $P'(t)$ 在连续 $n$ 天内为负，表示持续收敛
    - 若 $P(t)$ 小于某阈值，表示非常接近，趋于稳定
    """)
    
    # # 用户设置
    # window_length = st.slider("📆 收敛持续时间长度（天）", min_value=2, max_value=30, value=5)
    # threshold = st.number_input("🔽 收敛阈值 P(t) < ", value=0.5, step=0.1)

    # # 计算 P(t)
    # df["P"] = (df["MA_5"] - df["MA_10"])**2 + (df["MA_10"] - df["MA_20"])**2 + (df["MA_5"] - df["MA_20"])**2

    # # 按股票分组，计算导数 P'(t)
    # df = df.sort_values(["股票代码", "日期"])
    # df["P_diff"] = df.groupby("股票代码")["P"].diff()

    # # 寻找收敛股票：连续 window_length 天 P'(t)<0 且 P(t)<threshold
    # def is_converging(group):
    #     group = group.dropna(subset=["P_diff", "P"])
    #     if len(group) < window_length:
    #         return False
    #     last_n = group.tail(window_length)
    #     return all(last_n["P_diff"] < 0) and all(last_n["P"] < threshold)

    # # 筛选收敛股票
    # converging_stocks = []
    # for code, group in df.groupby("股票代码"):
    #     if is_converging(group):
    #         converging_stocks.append(code)

    # st.success(f"🎯 满足条件的收敛股票数量：{len(converging_stocks)}")
    # st.dataframe(pd.DataFrame({"股票代码": converging_stocks}))

    # # 可视化选项
    # selected_stock = st.selectbox("📌 选择股票代码查看 P(t) 收敛情况", options=sorted(df["股票代码"].unique()))
    # if selected_stock:
    #     stock_df = df[df["股票代码"] == selected_stock].copy()

    #     fig, ax = plt.subplots(figsize=(10, 4))
    #     ax.plot(stock_df["日期"], stock_df["P"], label="P(t)")
    #     ax.plot(stock_df["日期"], stock_df["P_diff"], label="P'(t)", linestyle="--")
    #     ax.axhline(threshold, color='red', linestyle=':', label="Threshold")
    #     ax.set_title(f"股票 {selected_stock} 的 P(t) 及导数变化")
    #     ax.legend()
    #     st.pyplot(fig)



    # 原来的：
    # min_date = stock_df["日期"].min()
    # max_date = stock_df["日期"].max()
    
    # 修改为：


    # 用户设置
    st.header("参数设置")
    window_length = st.slider("📆 连续收敛时间长度（天）", min_value=2, max_value=30, value=5)
    threshold = st.number_input("🎯 收敛强度阈值 P(t) <", value=0.5, step=0.1)

    # 计算 P(t)
    df = df.sort_values(["股票代码", "日期"])
    df["P"] = (df["MA_5"] - df["MA_10"])**2 + (df["MA_10"] - df["MA_20"])**2 + (df["MA_5"] - df["MA_20"])**2
    df["P_diff"] = df.groupby("股票代码")["P"].diff()

    # 判断是否收敛
    def is_converging(group):
        group = group.dropna(subset=["P_diff", "P"])
        if len(group) < window_length:
            return False
        last_n = group.tail(window_length)
        return all(last_n["P_diff"] < 0) and all(last_n["P"] < threshold)

    # 筛选股票
    converging_stocks = []
    for code, group in df.groupby("股票代码"):
        if is_converging(group):
            converging_stocks.append(code)

    st.success(f"✅ 符合收敛条件的股票数量：{len(converging_stocks)}")
    st.dataframe(pd.DataFrame({"股票代码": converging_stocks}))

    # 可视化部分
    selected_code = st.selectbox("🔍 选择查看收敛趋势的股票代码", options=sorted(df["股票代码"].unique()))
    stock_df = df[df["股票代码"] == selected_code].copy()

    # 显示时间范围选择
    min_date = stock_df["日期"].min().date()
    max_date = stock_df["日期"].max().date()
    start_date, end_date = st.slider(
    "📅 选择可视化时间范围",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
    )

    # 选完日期后再转换回 Timestamp 进行过滤
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    stock_df = stock_df[(stock_df["日期"] >= start_date) & (stock_df["日期"] <= end_date)]

    # 可视化 P(t)
    st.subheader("📊 P(t) 及导数趋势")
    chart_data = stock_df.set_index("日期")[["P", "P_diff"]]
    st.line_chart(chart_data)
