import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RPS & 波动率分析", layout="wide")
st.title("📊 股票RPS与波动率分析工具")

uploaded_file = st.file_uploader(
    "📂 上传CSV文件（需含 '日期', '股票代码', '收盘价'）", 
    type=["csv"],
    key="file_uploader"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 数据预处理
    df["日期"] = pd.to_datetime(df["日期"])
    df["股票代码"] = df["股票代码"].astype(str).str.extract(r'(\d{6})')  # 提取6位数字代码

    required_cols = {"日期", "股票代码", "收盘价"}
    if not required_cols.issubset(df.columns):
        st.error("❌ 缺少必要列：'日期', '股票代码', '收盘价'")
        st.stop()

    # 设置周期参数
    periods = [10, 20, 30, 60, 90]

    # 侧边栏设置
    vol_period = st.sidebar.selectbox(
        "选择波动率计算周期（天）", 
        [30, 60, 90], 
        index=2,
        key="vol_period_select"
    )

    latest_date = df["日期"].max()

    # 指标计算函数
    def calc_metrics(group):
        group = group.sort_values("日期")
        res = {"股票代码": group["股票代码"].iloc[0]}

        for p in periods:
            recent = group[group["日期"] <= latest_date].tail(p)
            if len(recent) < p:
                res[f"涨幅{p}"] = np.nan
                res[f"RPS{p}"] = np.nan
            else:
                start = recent["收盘价"].iloc[0]
                end = recent["收盘价"].iloc[-1]
                change = (end - start) / start * 100
                res[f"涨幅{p}"] = change
                res[f"RPS{p}"] = change  # 后续再统一替换为百分位排名

        returns = group["收盘价"].pct_change().dropna()
        recent_ret = returns[-vol_period:]
        res[f"波动率{vol_period}"] = (
            recent_ret.std() * np.sqrt(252) if len(recent_ret) >= vol_period else np.nan
        )

        return pd.Series(res)

    # 应用函数
    result_df = df.groupby("股票代码").apply(calc_metrics).reset_index(drop=True)

    # 替换为RPS百分位排名
    for p in periods:
        result_df[f"RPS{p}"] = result_df[f"RPS{p}"].rank(pct=True) * 100

    # 排序字段选择（所有除“股票代码”的字段）
    sort_column = st.selectbox(
        "🔢 选择排序依据", 
        result_df.columns.difference(["股票代码"]).tolist(), 
        key="sort_column_select"
    )

    # 排序顺序选择
    sort_order = st.radio(
        "📈 选择排序顺序", 
        ["降序（从大到小）", "升序（从小到大）"], 
        horizontal=True,
        key="sort_order_radio"
    )
    ascending = sort_order == "升序（从小到大）"

    # 排序并展示结果
    top_df = result_df.sort_values(sort_column, ascending=ascending).head(100).reset_index(drop=True)

    st.markdown(f"### 📈 按 **{sort_column}** 排序的前100只股票")
    st.dataframe(top_df.style.background_gradient(axis=0, cmap="Blues"), use_container_width=True)
