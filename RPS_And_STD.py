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
# 显示计算公式说明
with st.expander("📚 查看RPS与波动率的计算方法"):
    st.markdown("### 📌 RPS（Relative Price Strength）")
    st.markdown(
        r"""
        RPS是衡量一只股票在某一段时间内涨幅相对于所有股票涨幅的相对强弱。其计算流程如下：

        1. 对于每只股票，计算在周期 $( p )$ 内的涨幅：
        $$
        \text{涨幅}_p = \frac{P_{\text{end}} - P_{\text{start}}}{P_{\text{start}}} \times 100
        $$
        其中 $( P_{\text{start}})$ 和 $( P_{\text{end}} )$ 分别是周期起始和结束时的收盘价。

        2. 将所有股票的涨幅进行百分位排名，得到RPS值（范围为0-100）：
        $$
        \text{RPS}_p = \text{percentile\_rank}(\text{涨幅}_p)
        $$

        RPS越高表示该股票相对于其他股票表现越强。
        """
    )

    st.markdown("### 📌 波动率（年化标准差）")
    st.markdown(
        r"""
        波动率用于衡量股票收益的变动幅度，公式如下：

        $$
        \sigma_{\text{annual}} = \text{std}(r_{1}, r_{2}, \dots, r_{n}) \times \sqrt{252}
        $$
        其中 $( r_i )$ 为每日收益率（对数或简单收益），252为一年交易日数量。

        简单收益率定义为：
        $$
        r_t = \frac{P_t - P_{t-1}}{P_{t-1}}
        $$

        波动率越高代表股票价格的不确定性越高，风险也越大。
        """
    )
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, dtype={'股票代码': str})

    # 数据预处理
    df["日期"] = pd.to_datetime(df["日期"])
    # df["股票代码"] = df["股票代码"].astype(str).str.extract(r'(\d{6})')  # 提取6位数字代码
    # df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    # df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    required_cols = {"日期", "股票代码", "收盘价"}
    if not required_cols.issubset(df.columns):
        st.error("❌ 缺少必要列：'日期', '股票代码', '收盘价'")
        st.stop()

    # 设置周期参数
    periods = [10, 20, 30, 60, 90]

    # 侧边栏设置
    vol_period = st.sidebar.selectbox(
        "选择波动率计算周期（天）", 
        [10, 20, 30, 40, 50, 60, 70, 80, 90], 
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


    st.markdown("---")
    st.markdown("### 🔁 二次排序设置（可选）")
    
    # 二次排序字段选择
    secondary_sort_column = st.selectbox(
        "🔂 选择二次排序依据", 
        result_df.columns.difference(["股票代码"]).tolist(), 
        key="secondary_sort_column_select"
    )
    
    # 二次排序顺序选择
    secondary_sort_order = st.radio(
        "⬇️ 二次排序顺序", 
        ["降序（从大到小）", "升序（从小到大）"], 
        horizontal=True,
        key="secondary_sort_order_radio"
    )
    secondary_ascending = secondary_sort_order == "升序（从小到大）"
    
    # 应用二次排序
    top_df = top_df.sort_values(
        by=secondary_sort_column,
        ascending=secondary_ascending
    ).reset_index(drop=True)
    st.markdown(f"### 📈 按 **{secondary_sort_column}** 二次排序的100只股票")    
    st.dataframe(top_df.style.background_gradient(axis=0, cmap="Blues"), use_container_width=True)
