import streamlit as st
import pandas as pd

st.set_page_config(page_title="最可能上涨的股票筛选器", layout="wide")

st.title("📈 最可能上涨的股票筛选器")
st.write("上传包含多个股票数据的 CSV 文件，系统将自动计算每支股票的上涨得分。")

# 上传文件
uploaded_file = st.file_uploader("📤 上传包含多支股票的CSV文件", type=["csv"])

if uploaded_file:
    # 读取数据
    df = pd.read_csv(uploaded_file)
    
    # 确保格式正确
    required_cols = {'日期','开盘价','收盘价','成交量','股票代码'}
    if not required_cols.issubset(set(df.columns)):
        st.error(f"❌ 缺少必要列，请确保CSV包含以下列: {required_cols}")
    else:
        # 日期列转为日期格式
        df['日期'] = pd.to_datetime(df['日期'])

        # 主逻辑函数
        def calculate_signals(df):
            df = df.sort_values('日期')
            df['阳线'] = (df['收盘价'] > df['开盘价']).astype(int)
            df['5日均价'] = df['收盘价'].rolling(window=5).mean()
            df['放量'] = df['成交量'] > df['成交量'].rolling(window=5).mean()
            df['站上均线'] = df['收盘价'] > df['5日均价']
            
            score = (
                df['阳线'].tail(5).sum() +
                df['站上均线'].tail(1).sum() +
                df['放量'].tail(1).sum()
            )
            return score

        def select_top_stocks(data):
            scores = data.groupby('股票代码').apply(calculate_signals)
            return scores.sort_values(ascending=False)

        # 执行
        with st.spinner("正在分析，请稍候..."):
            result = select_top_stocks(df)
            st.success("✅ 分析完成！")

            # 展示结果
            st.subheader("📊 股票上涨得分排行")
            st.dataframe(result.reset_index().rename(columns={0: "上涨得分"}))

            # 下载按钮
            csv = result.reset_index().rename(columns={0: "上涨得分"}).to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 下载结果 CSV", data=csv, file_name='up_stock_score.csv', mime='text/csv')
