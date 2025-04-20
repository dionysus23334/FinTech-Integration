import streamlit as st
import pandas as pd
import altair as alt

st.title("📈 公告事件与收盘价（Altair 交互式图表）")

# 上传文件
events_file = st.file_uploader("📄 上传公告数据 CSV", type=["csv"])
prices_file = st.file_uploader("📊 上传股票价格数据 CSV", type=["csv"])

if events_file and prices_file:

    prices_df = pd.read_csv(prices_file, dtype={'股票代码': str})
    events_df = pd.read_csv(events_file, dtype={'股票代码': str}).drop(columns=['Unnamed: 0'])
    
    # 股票代码清洗为6位字符串
    # prices_df['股票代码'] = prices_df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True).str.zfill(6)

    # 选择要展示的股票
    stock_codes = prices_df['股票代码'].unique()
    selected_code = st.selectbox("请选择股票代码", stock_codes)

    # 筛选并处理日期
    df = prices_df[prices_df['股票代码'] == selected_code].copy()
    df['日期'] = pd.to_datetime(df['日期'])
    events_df['公告日期'] = pd.to_datetime(events_df['公告日期'])

    # 过滤出该股票的事件
    # stock_events = events_df[events_df['股票代码'] == selected_code].copy()
    
    st.dataframe(events_df)
    stock_events = events_df
    
    # Altair brush 选择器
    brush = alt.selection(type='interval', encodings=['x'])

    # 可视化字段选择（只列出数值型列，排除“股票代码”等）
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    value_columns = st.multiselect("📊 请选择要可视化的字段（支持多选）", numeric_columns, default=['收盘价'])
    
    # 颜色列表
    color_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
        '#bcbd22', '#17becf'
    ]
    
    # 构造多列折线图
    lines = []
    for i, col in enumerate(value_columns):
        color = color_palette[i % len(color_palette)]
        line = alt.Chart(df).mark_line().encode(
            x='日期:T',
            y=alt.Y(f'{col}:Q', title='数值'),
            color=alt.value(color),
            tooltip=['日期:T', alt.Tooltip(f'{col}:Q', title=col)]
        ).properties()
        lines.append(line)
    
    # 合并所有折线
    price_line = alt.layer(*lines).properties(
        width=800,
        height=300,
        title=f'{selected_code} 股票数值走势（多字段）'
    )

    # 为事件编号（从1开始）
    stock_events = stock_events.reset_index(drop=True)
    stock_events['事件编号'] = stock_events.index + 1
    
    # 事件竖线图（rule）
    event_lines = alt.Chart(stock_events).mark_rule(color='red').encode(
        x='公告日期:T',
        tooltip=['事件编号:N', '公告标题:N']
    )
    
    # 编号文字图，放在收盘价最大值上方一点
    event_labels = alt.Chart(stock_events).mark_text(
        align='center',
        dy=-10,
        fontSize=12,
        color='red'
    ).encode(
        x='公告日期:T',
        y=alt.value(df['收盘价'].max() * 1.03),  # 固定放在曲线上方
        text='事件编号:N'
    )
    
    # 将事件线和编号叠加到主图上
    final_chart = (
        price_line +
        event_lines +
        event_labels
    ).interactive().properties(
        width=800,
        height=300,
        title=f'{selected_code} 收盘价走势及公告事件（红线标注）'
    ).configure_title(
        fontSize=16,
        anchor='start'
    )
    
    # 显示图表

    st.altair_chart(final_chart, use_container_width=True)
