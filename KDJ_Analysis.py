import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# KDJ 计算函数
def calculate_kdj(df, n=9, m1=3, m2=3):
    df = df.copy()
    df["low_n"] = df["最低价"].rolling(window=n, min_periods=1).min()
    df["high_n"] = df["最高价"].rolling(window=n, min_periods=1).max()
    df["RSV"] = (df["收盘价_flow"] - df["low_n"]) / (df["high_n"] - df["low_n"]) * 100

    df["K"] = 0.0
    df["D"] = 0.0
    df.loc[df.index[0], "K"] = 50
    df.loc[df.index[0], "D"] = 50

    for i in range(1, len(df)):
        df.loc[df.index[i], "K"] = (m1 - 1)/m1 * df.loc[df.index[i - 1], "K"] + 1/m1 * df.loc[df.index[i], "RSV"]
        df.loc[df.index[i], "D"] = (m2 - 1)/m2 * df.loc[df.index[i - 1], "D"] + 1/m2 * df.loc[df.index[i], "K"]

    df["J"] = 3 * df["K"] - 2 * df["D"]
    return df

# Streamlit 页面设置
st.set_page_config(page_title="KDJ 指标计算器", layout="wide")
st.title("📈 股票 KDJ 指标分析工具")
st.write("上传包含 '日期', '最高价', '最低价', '收盘价_flow' 列的 CSV 文件。")

# 上传文件
uploaded_file = st.file_uploader("上传CSV文件", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, dtype={'股票代码': str})

    required_columns = {'日期', '最高价', '最低价', '收盘价_flow'}
    if not required_columns.issubset(df.columns):
        st.error(f"CSV文件必须包含以下列：{', '.join(required_columns)}")
    else:
        df['日期'] = pd.to_datetime(df['日期'])
        # 添加滑动条：选取最近 N 天数据
        max_days = len(df)
        days = st.slider("选择展示最近的天数", min_value=10, max_value=max_days, value=30, step=1)
        # ➕ 仅保留最近30天数据
        df_recent = df.tail(days)
        df_kdj = calculate_kdj(df_recent)
        
        st.subheader(f"📉 最近{d}天收盘价曲线")
        # 计算 Y 轴上下限
        y_min = df_kdj['最低价'].min()
        y_max = df_kdj['最高价'].max()
        
        # 创建 Altair 图表
        price_chart = alt.Chart(df_kdj).mark_line(color='blue').encode(
            x='日期:T',
            y=alt.Y('收盘价_flow:Q', scale=alt.Scale(domain=[y_min, y_max]))
        ).properties(
            width=700,
            height=300,
            title="收盘价曲线（最近30天）"
        )
        
        st.altair_chart(price_chart, use_container_width=True)
        
      

        st.subheader(f"📊 最近{d}天 KDJ 曲线")
        chart_data_kdj = df_kdj.set_index('日期')[['K', 'D', 'J']]
        st.line_chart(chart_data_kdj)

        with st.expander("📋 展开查看KDJ数据表格"):
            st.dataframe(df_kdj[["日期", "收盘价_flow", "K", "D", "J"]].reset_index(drop=True))


