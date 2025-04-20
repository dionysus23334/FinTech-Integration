import streamlit as st
import pandas as pd

st.set_page_config(page_title="股票均线展示", layout="wide")
st.title("📈 股票均线可视化工具")

# 上传均线文件
uploaded_file = st.file_uploader("📤 上传已包含均线数据的CSV文件（需包含 '日期', '股票代码', 'MA_5', 'MA_10', 'MA_20' 列）", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["日期"])
    df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    st.success(f"✅ 已加载数据，共 {df['股票代码'].nunique()} 支股票")

    # 展示数据
    with st.expander("📋 展示全部均线数据"):
        st.dataframe(df)

    # 股票选择器
    st.subheader("📌 选择股票代码查看其均线图")
    stock_list = sorted(df['股票代码'].unique())
    selected_stock = st.selectbox("请选择股票代码", stock_list)

    df_selected = df[df['股票代码'] == selected_stock].sort_values(by="日期")

    # 绘制均线图
    st.line_chart(
        df_selected.set_index('日期')[['MA_5', 'MA_10', 'MA_20']],
        use_container_width=True
    )
