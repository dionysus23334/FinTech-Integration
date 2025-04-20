import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 设置页面标题
st.set_page_config(page_title="股票均线分析", layout="wide")
st.title("📈 股票5日/10日/20日均线分析工具")

# 上传CSV文件
uploaded_file = st.file_uploader("请上传包含多个股票的CSV文件（必须包含‘日期’, ‘股票代码’, ‘收盘价’）", type=['csv'])

if uploaded_file is not None:
    # 读取CSV
    df = pd.read_csv(uploaded_file, parse_dates=['日期'])
    
    # 标准化股票代码格式
    df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    df['股票代码'] = df['股票代码'].astype(str).str.ljust(6, "0")

    # 批量计算均线
    def calculate_all_stocks_averages(data: pd.DataFrame) -> pd.DataFrame:
        results = []
        stock_codes = data['股票代码'].unique()

        for stock_code in stock_codes:
            df_stock = data[data['股票代码'] == stock_code].copy()
            df_stock['日期'] = pd.to_datetime(df_stock['日期'])
            df_stock = df_stock.sort_values(by='日期').reset_index(drop=True)

            df_stock['MA_5'] = df_stock['收盘价'].rolling(window=5, min_periods=5).mean()
            df_stock['MA_10'] = df_stock['收盘价'].rolling(window=10, min_periods=10).mean()
            df_stock['MA_20'] = df_stock['收盘价'].rolling(window=20, min_periods=20).mean()

            df_stock = df_stock[df_stock['MA_20'].notna()].copy()
            df_stock['股票代码'] = stock_code

            results.append(df_stock[['日期', '股票代码', 'MA_5', 'MA_10', 'MA_20']])

        df_result = pd.concat(results, ignore_index=True)
        df_result = df_result.sort_values(by='日期', ascending=False).reset_index(drop=True)
        return df_result

    df_averages = calculate_all_stocks_averages(df)

    st.success(f"✅ 已成功计算 {df_averages['股票代码'].nunique()} 只股票的均线数据。")

    # 展示均线数据表
    with st.expander("📋 展示全部均线数据（可筛选、搜索）"):
        st.dataframe(df_averages)

    # 股票选择 + 可视化
    st.subheader("🔍 查看某只股票的均线走势图")

    selected_code = st.selectbox("请选择要查看的股票代码", sorted(df_averages['股票代码'].unique()))

    df_selected = df_averages[df_averages['股票代码'] == selected_code].sort_values(by='日期')

    # 绘图
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_selected['日期'], df_selected['MA_5'], label='MA 5日')
    ax.plot(df_selected['日期'], df_selected['MA_10'], label='MA 10日')
    ax.plot(df_selected['日期'], df_selected['MA_20'], label='MA 20日')

    ax.set_title(f"{selected_code} 股票均线走势")
    ax.set_xlabel("日期")
    ax.set_ylabel("价格")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

