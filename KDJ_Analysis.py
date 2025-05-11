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
    df["日期"] = pd.to_datetime(df["日期"])
    df = df.sort_values("日期")

    # 计算 KDJ
    df_kdj = calculate_kdj(df)

    # 画图
    st.subheader("📉 收盘价趋势图")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(df_kdj["日期"], df_kdj["收盘价_flow"], label="收盘价", color="blue")
    ax1.set_xlabel("日期")
    ax1.set_ylabel("价格")
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("📊 KDJ 指标图")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(df_kdj["日期"], df_kdj["K"], label="K", color="green")
    ax2.plot(df_kdj["日期"], df_kdj["D"], label="D", color="orange")
    ax2.plot(df_kdj["日期"], df_kdj["J"], label="J", color="red")
    ax2.set_xlabel("日期")
    ax2.set_ylabel("指标值")
    ax2.legend()
    st.pyplot(fig2)

    # 显示数据表
    with st.expander("🔍 查看KDJ数据表"):
        st.dataframe(df_kdj[["日期", "收盘价_flow", "K", "D", "J"]].reset_index(drop=True))
