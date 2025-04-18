import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RPS & 波动率分析", layout="wide")
st.title("📊 股票RPS与波动率分析工具")

uploaded_file = st.file_uploader("📂 上传CSV文件（需含 '日期', '股票代码', '收盘价'）", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 数据预处理
    df["日期"] = pd.to_datetime(df["日期"])
    df["股票代码"] = df["股票代码"].astype(str)  # 转换成字符串
    df["股票代码"] = df["股票代码"].str.replace(r"^[0-9]+\.", "", regex=True)  # 去掉前面的 "1."、"0." 等前缀
    df["股票代码"] = df["股票代码"].str.zfill(6)

    required_cols = {"日期", "股票代码", "收盘价"}
    if not required_cols.issubset(df.columns):
        st.error("❌ 缺少必要列：'日期', '股票代码', '收盘价'")
        st.stop()

    # 用户设置项
    periods = [10, 20, 30, 60, 90]
    vol_period = st.sidebar.selectbox("选择波动率计算周期（天）", [30, 60, 90], index=2)
    rps_sort_period = st.sidebar.selectbox("选择RPS排序周期", periods, index=4)

    latest_date = df["日期"].max()
    result_rows = []

    for stock_code in df["股票代码"].unique():
        stock_df = df[df["股票代码"] == stock_code].sort_values("日期")
        row = {"股票代码": stock_code}

        for period in periods:
            recent = stock_df[stock_df["日期"] <= latest_date].tail(period)
            if len(recent) < period:
                row[f"RPS{period}"] = np.nan
                row[f"涨幅{period}"] = np.nan
                continue
            start_price = recent.iloc[0]["收盘价"]
            end_price = recent.iloc[-1]["收盘价"]
            pct_change = (end_price - start_price) / start_price * 100
            row[f"涨幅{period}"] = pct_change
            row[f"RPS{period}"] = pct_change  # 暂存，稍后进行排名替换

        # 波动率计算
        stock_df = stock_df.set_index("日期").sort_index()
        returns = stock_df["收盘价"].pct_change().dropna()
        recent_returns = returns[-vol_period:]
        row[f"波动率{vol_period}"] = recent_returns.std() * np.sqrt(252) if len(recent_returns) >= vol_period else np.nan

        result_rows.append(row)

    result_df = pd.DataFrame(result_rows)

    # 对RPS列进行百分位排名
    for period in periods:
        result_df[f"RPS{period}"] = result_df[f"RPS{period}"].rank(pct=True) * 100

    # 排序并显示前100名
    sort_column = st.selectbox("🔢 选择排序依据", [f"RPS{rps_sort_period}", f"波动率{vol_period}"])
    top_df = result_df.sort_values(sort_column, ascending=False).head(100).reset_index(drop=True)

    st.markdown(f"### 📈 按 **{sort_column}** 排序的前100只股票")
    st.dataframe(top_df.style.background_gradient(axis=0, cmap="Blues"), use_container_width=True)
