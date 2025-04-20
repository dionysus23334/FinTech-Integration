
import streamlit as st
import pandas as pd

st.set_page_config(page_title="股票均线查看器", layout="wide")
st.title("📈 股票均线可视化工具")

# 上传文件
uploaded_file = st.file_uploader("📤 上传已包含均线数据的CSV文件（需含'日期','股票代码','MA_5','MA_10','MA_20'）", type=["csv"])

if uploaded_file is not None:
    # 读取数据
    df = pd.read_csv(uploaded_file, parse_dates=["日期"])
    df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    # 展示全部股票数量
    st.success(f"✅ 数据加载成功，共 {df['股票代码'].nunique()} 支股票")

    # 股票选择
    stock_list = sorted(df['股票代码'].unique())
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
