import streamlit as st
import pandas as pd

# 均线计算函数
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


# Streamlit 应用主体
st.title("多股票均线计算器")

uploaded_file = st.file_uploader("上传股票K线CSV文件（含：日期、股票代码、收盘价）", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=['日期'], dtype={'股票代码': str})
        df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
        df['股票代码'] = df['股票代码'].str.ljust(6, '0')

        st.success("文件上传成功，正在计算均线...")
        df_result = calculate_all_stocks_averages(df)

        st.write("部分结果预览：", df_result.head())

        csv = df_result.to_csv(index=False).encode('utf-8-sig')
        st.download_button("下载结果 CSV", data=csv, file_name="均线结果.csv", mime="text/csv")

    except Exception as e:
        st.error(f"出错了：{e}")
