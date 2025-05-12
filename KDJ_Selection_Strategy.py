import streamlit as st
import pandas as pd
import altair as alt

# KDJ 计算函数
def calculate_kdj(df, n=9, m1=3, m2=3):
    df = df.copy()
    df["low_n"] = df["最低价"].rolling(window=n, min_periods=1).min()
    df["high_n"] = df["最高价"].rolling(window=n, min_periods=1).max()
    df["RSV"] = (df["收盘价_flow"] - df["low_n"]) / (df["high_n"] - df["low_n"]) * 100

    df["K"] = 50.0
    df["D"] = 50.0

    for i in range(1, len(df)):
        df.loc[df.index[i], "K"] = (m1 - 1) / m1 * df.loc[df.index[i - 1], "K"] + 1 / m1 * df.loc[df.index[i], "RSV"]
        df.loc[df.index[i], "D"] = (m2 - 1) / m2 * df.loc[df.index[i - 1], "D"] + 1 / m2 * df.loc[df.index[i], "K"]

    df["J"] = 3 * df["K"] - 2 * df["D"]
    df["P"] = df["K"] - df["D"]
    df["P_diff"] = df["P"].diff()
    return df

# Streamlit 设置
st.set_page_config(page_title="KDJ 筛选器", layout="wide")
st.title("📈 股票 KDJ 指标分析工具")

# 上传 CSV 文件
uploaded_file = st.file_uploader("📤 上传包含 '日期', '股票代码', '最高价', '最低价', '收盘价_flow' 的CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, dtype={"股票代码": str})
    required_columns = {'日期', '最高价', '最低价', '收盘价_flow', '股票代码'}

    if not required_columns.issubset(df.columns):
        st.error(f"❌ CSV必须包含列：{', '.join(required_columns)}")
    else:
        df['日期'] = pd.to_datetime(df['日期'])
        df = df.sort_values(["股票代码", "日期"])

        # 对每支股票计算KDJ
        kdj_list = []
        for code, group in df.groupby("股票代码"):
            kdj = calculate_kdj(group)
            kdj["股票代码"] = code
            kdj_list.append(kdj)
        df_kdj_all = pd.concat(kdj_list).reset_index(drop=True)

        # 侧边栏控制项
        st.sidebar.header("🔍 筛选条件")
        lookback_days = st.sidebar.slider("最近N天检测", min_value=3, max_value=60, value=10)
        p_threshold = st.sidebar.number_input("P阈值（P必须 < 此值）", value=0.0)
        require_upward = st.sidebar.checkbox("要求P整体上升（最后一天大于第一天）", value=True)

        # 筛选满足条件的股票
        result_dfs = []
        for code, group in df_kdj_all.groupby("股票代码"):
            group_sorted = group.sort_values("日期").copy()
            recent = group_sorted.tail(lookback_days)

            if len(recent) < lookback_days:
                continue

            all_p_negative = (recent["P"] < p_threshold).all()
            upward = recent["P"].iloc[-1] > recent["P"].iloc[0]

            if all_p_negative and (not require_upward or upward):
                result_dfs.append(recent.assign(股票代码=code))

        # 显示结果
        st.subheader(f"🎯 满足最近 {lookback_days} 天 P < {p_threshold}" +
                     (" 且P整体上升" if require_upward else "") +
                     " 的股票")

        if not result_dfs:
            st.info("⚠️ 暂无符合条件的股票")
        else:
            final_result_df = pd.concat(result_dfs)

            selected_code = st.selectbox("选择股票代码查看详情", final_result_df["股票代码"].unique())
            selected_df = final_result_df[final_result_df["股票代码"] == selected_code]

            st.markdown(f"#### 股票代码：{selected_code}")
            st.dataframe(selected_df.reset_index(drop=True))

            st.altair_chart(
                alt.Chart(selected_df).transform_fold(
                    ['K', 'D', 'J']
                ).mark_line().encode(
                    x='日期:T',
                    y='value:Q',
                    color='key:N'
                ).properties(width=800, height=400, title=f"{selected_code} 的 KDJ 曲线"),
                use_container_width=True
            )
            
            # 获取唯一的股票代码列表
            matched_codes = final_result_df["股票代码"].unique()
            matched_codes_df = pd.DataFrame(matched_codes, columns=["股票代码"])
            
            # 显示股票代码列表
            st.markdown("### ✅ 满足条件的股票代码列表")
            st.write(matched_codes_df)
            
            # 添加导出按钮
            csv = matched_codes_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 下载股票代码列表 CSV",
                data=csv,
                file_name=f"matched_stocks_last{lookback_days}days.csv",
                mime='text/csv'
            )

