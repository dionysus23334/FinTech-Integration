
import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 市值排名", layout="centered")
st.title("🏦 股票市值排行榜")

# 上传 CSV 文件
uploaded_file = st.file_uploader("请上传包含 股票代码 / 总市值 / 流通市值 的 CSV 文件", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, dtype={"股票代码": str})

        # 基本检查
        required_cols = {"股票代码", "总市值", "流通市值"}
        if not required_cols.issubset(df.columns):
            st.error(f"❌ 缺少必要列：{required_cols - set(df.columns)}")
        else:
            # 排序方式选择
            sort_by = st.radio("请选择排序方式", ["总市值", "流通市值"], horizontal=True)

            # 排序处理
            sorted_df = df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)
            sorted_df.index += 1  # 从1开始编号

            # 显示完整表格
            st.dataframe(sorted_df.style.format({
                "总市值": "{:,.2f}",
                "流通市值": "{:,.2f}"
            }), use_container_width=True)

            # Top-N 控制
            top_n = st.slider("查看前 N 名", min_value=1, max_value=len(df), value=10)
            st.subheader(f"📈 Top {top_n} 股票（按{sort_by}）")
            st.table(sorted_df.head(top_n).style.format({
                "总市值": "{:,.2f}",
                "流通市值": "{:,.2f}"
            }))

    except Exception as e:
        st.error(f"文件读取出错：{e}")
else:
    st.info("📤 请上传 CSV 文件以开始查看市值排名")

