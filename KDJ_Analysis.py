import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

        df_kdj = calculate_kdj(df)
        
        # ➕ 仅保留最近30天数据
        df_kdj = df_kdj.head(30)

        
        st.subheader("📉 收盘价曲线")
        chart_data_price = df_kdj.set_index('日期')[['收盘价_flow']]
        st.line_chart(chart_data_price)

        st.subheader("📊 KDJ 曲线")
        chart_data_kdj = df_kdj.set_index('日期')[['K', 'D', 'J']]
        st.line_chart(chart_data_kdj)

        with st.expander("📋 展开查看KDJ数据表格"):
            st.dataframe(df_kdj)


    # 显示数据表
    with st.expander("🔍 查看KDJ数据表"):
        st.dataframe(df_kdj[["日期", "收盘价_flow", "K", "D", "J"]].reset_index(drop=True))
