import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore

st.title("📊 股票RPS与波动率分析")

uploaded_file = st.file_uploader("上传你的CSV文件", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["日期"] = pd.to_datetime(df["日期"])
    
    if not all(col in df.columns for col in ["日期", "股票代码", "收盘价"]):
        st.error("CSV中必须包含 '日期', '股票代码', '收盘价'")
        st.stop()
    
    df = df.sort_values(["股票代码", "日期"]).reset_index(drop=True)

    periods = [10, 20, 30, 60, 90]
    latest_date = df["日期"].max()

    result_rows = []

    for stock_code in df["股票代码"].unique():
        stock_df = df[df["股票代码"] == stock_code].sort_values("日期")
        row = {"股票代码": stock_code}

        for period in periods:
            recent = stock_df[stock_df["日期"] <= latest_date].tail(period)
            if len(recent) < period:
                row[f"RPS{period}"] = np.nan
                continue
            start_price = recent.iloc[0]["收盘价"]
            end_price = recent.iloc[-1]["收盘价"]
            pct_change = (end_price - start_price) / start_price * 100
            row[f"涨幅{period}"] = pct_change
            # 暂存，稍后再计算RPS
            row[f"_pct{period}"] = pct_change

        # 90天波动率
        if len(stock_df[stock_df["日期"] <= latest_date].tail(91)) >= 91:
            stock_df = stock_df.set_index("日期").sort_index()
            returns = stock_df["收盘价"].pct_change().dropna().tail(90)
            row["波动率90"] = returns.std() * np.sqrt(252)  # annualized
        else:
            row["波动率90"] = np.nan

        result_rows.append(row)

    result_df = pd.DataFrame(result_rows)

    # 计算RPS（用百分位排名）
    for period in periods:
        pct_column = f"_pct{period}"
        if pct_column in result_df.columns:
            result_df[f"RPS{period}"] = result_df[pct_column].rank(pct=True) * 100

    # 丢弃中间列
    result_df = result_df.drop(columns=[f"_pct{p}" for p in periods])

    st.dataframe(result_df.sort_values("RPS90", ascending=False).reset_index(drop=True))

    selected_sort = st.selectbox("选择排序依据", ["RPS10", "RPS20", "RPS30", "RPS60", "RPS90", "波动率90"])
    st.dataframe(result_df.sort_values(selected_sort, ascending=False).reset_index(drop=True))
