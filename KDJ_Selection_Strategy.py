import streamlit as st
import pandas as pd

st.title("筛选满足 a < K-D < b 的股票")

# 上传CSV
uploaded_file = st.file_uploader("上传包含KDJ数据的CSV文件", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    # 必须包含这些列
    required_cols = {"stock_code", "date", "K", "D"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV缺少必要列：{required_cols}")
    else:
        # 用户输入区间[a, b]
        a = st.number_input("请输入a (下限)", value=-10.0)
        b = st.number_input("请输入b (上限)", value=0.0)

        # 是否筛选导数 > 0 的点
        filter_derivative = st.checkbox("进一步筛选K-D导数为正")

        # 计算每一行的P = K - D
        df["P"] = df["K"] - df["D"]

        # 按股票代码分组处理
        grouped = df.sort_values("date").groupby("stock_code")

        for stock_code, group in grouped:
            group = group.copy()
            group["P_diff"] = group["P"].diff()

            # 应用区间筛选
            filtered = group[(group["P"] > a) & (group["P"] < b)]
            
            if filter_derivative:
                filtered = filtered[filtered["P_diff"] > 0]

            if not filtered.empty:
                st.subheader(f"股票代码：{stock_code}")
                st.dataframe(filtered.reset_index(drop=True))
