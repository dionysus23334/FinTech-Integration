import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False    # 正负号

st.title("📈 公告事件与股价分析图")

# 上传文件
events_file = st.file_uploader("上传公告文件（如 600519Events.csv）", type=["csv"])
prices_file = st.file_uploader("上传价格文件（如 股票K线数据_90天.csv）", type=["csv"])

if events_file and prices_file:
    # 读取 CSV
    events_df = pd.read_csv(events_file)
    df = pd.read_csv(prices_file)

    # 处理股票代码
    df['股票代码'] = df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True)
    df['股票代码'] = df['股票代码'].astype(str).str.zfill(6)  # 保证6位，不足前补0

    # 用户选择股票代码
    stock_codes = df['股票代码'].unique()
    selected_code = st.selectbox("选择股票代码", stock_codes)

    prices_df = df[df['股票代码'] == selected_code]

    # 日期格式处理
    events_df['公告日期'] = pd.to_datetime(events_df['公告日期'], errors='coerce')
    prices_df['日期'] = pd.to_datetime(prices_df['日期'], errors='coerce')

    # 按日期排序
    prices_df = prices_df.sort_values(by='日期')

    # 画图逻辑
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(prices_df['日期'], prices_df['收盘价'], label='收盘价', color='blue')

    for idx, row in events_df.iterrows():
        event_date = row['公告日期']
        if pd.notnull(event_date) and event_date in prices_df['日期'].values:
            price = prices_df.loc[prices_df['日期'] == event_date, '收盘价'].values[0]
            ax.scatter(event_date, price, color='red', s=80, zorder=5)
            ax.text(event_date, price + 0.1, row['公告标题'], fontsize=8, rotation=45)

    ax.set_title(f'股票代码 {selected_code}：收盘价与公告事件')
    ax.set_xlabel('日期')
    ax.set_ylabel('收盘价')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
