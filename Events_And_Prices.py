import streamlit as st
import pandas as pd
import altair as alt

st.title("📈 公告事件与收盘价（Altair 交互式图表）")

# 上传文件
events_file = st.file_uploader("📄 上传公告数据 CSV", type=["csv"])
prices_file = st.file_uploader("📊 上传股票价格数据 CSV", type=["csv"])

if events_file and prices_file:

    prices_df = pd.read_csv(prices_file)
    events_df = pd.read_csv(events_file).drop(columns=['Unnamed: 0'])
    
    # 股票代码清洗为6位字符串
    prices_df['股票代码'] = prices_df['股票代码'].astype(str).str.replace(r'^[01]\.', '', regex=True).str.zfill(6)

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

    # 收盘价折线图 + brush
    price_line = alt.Chart(df).mark_line(color='steelblue').encode(
        x='日期:T',
        y='收盘价:Q',
        tooltip=['日期:T', '收盘价:Q']
    ).properties(
        width=800,
        height=300,
        title=f'{selected_code} 收盘价走势（可框选时间）'
    ).add_selection(
        brush
    )

    # 公告事件点图
    event_points = alt.Chart(stock_events).mark_circle(color='red', size=80).encode(
        x='公告日期:T',
        y=alt.value(df['收盘价'].max() * 1.02),  # 放在图上方
        tooltip=['公告日期:T', '公告标题:N']
    )

    # 合并两图
    chart = (price_line + event_points).interactive()
    st.altair_chart(chart)

    # 显示被选中的时间段内的事件
    st.subheader("📌 所选时间段内的公告事件")
    selected = alt.Chart(df).transform_filter(brush)

    # 获取 brush 所选时间段（Streamlit 无法直接从 Altair 获取 brush，需用 workaround）
    # 这里暂时手动选择日期范围
    start_date = st.date_input("开始日期", value=df['日期'].min().date())
    end_date = st.date_input("结束日期", value=df['日期'].max().date())

    if start_date and end_date:
        mask = (stock_events['公告日期'].dt.date >= start_date) & (stock_events['公告日期'].dt.date <= end_date)
        selected_events = stock_events[mask]
        if not selected_events.empty:
            st.dataframe(selected_events[['公告日期', '公告标题', '公告类型', '公告PDF链接']])
        else:
            st.info("该时间段内没有公告事件。")







    
    #     # 为事件编号（从1开始）
    # stock_events = stock_events.reset_index(drop=True)
    # stock_events['事件编号'] = stock_events.index + 1
    
    # # 事件竖线图（rule）
    # event_lines = alt.Chart(stock_events).mark_rule(color='red').encode(
    #     x='公告日期:T',
    #     tooltip=['事件编号:N', '公告标题:N']
    # ).properties(
    #     width=800,
    #     height=60
    # )
    
    # # 编号文字图
    # event_labels = alt.Chart(stock_events).mark_text(
    #     align='center',
    #     dy=-5,
    #     fontSize=12,
    #     color='black'
    # ).encode(
    #     x='公告日期:T',
    #     text='事件编号:N'
    # )
    
    # # 合并事件线和编号
    # event_timeline = (event_lines + event_labels).resolve_scale(y='independent')
    
    # # 上图：收盘价 + 点图
    # chart = (price_line + event_points).interactive()
    
    # # 总图表组合（上下堆叠）
    # final_chart = alt.vconcat(
    #     chart,
    #     event_timeline
    # ).configure_title(
    #     fontSize=16,
    #     anchor='start'
    # )
    
    # # 显示图表
    # st.altair_chart(final_chart, use_container_width=True)




    
    # 生成编号
    stock_events = stock_events.reset_index(drop=True)
    stock_events['事件编号'] = stock_events.index + 1
    
    # brush：交互式时间选择器
    brush = alt.selection_interval(encodings=["x"])
    
    # 折线图（收盘价）
    price_line = alt.Chart(df).mark_line(color='steelblue').encode(
        x='日期:T',
        y='收盘价:Q',
        tooltip=['日期:T', '收盘价:Q']
    )
    
    # 公告事件竖线
    event_lines = alt.Chart(stock_events).mark_rule(color='red').encode(
        x='公告日期:T',
        tooltip=['事件编号:N', '公告标题:N']
    )
    
    # 公告事件编号（数字标签）
    event_labels = alt.Chart(stock_events).mark_text(
        align='left',
        dy=-70,
        dx=3,
        fontSize=12,
        color='red'
    ).encode(
        x='公告日期:T',
        y=alt.value(df['收盘价'].max() * 1.02),
        text='事件编号:N'
    )
    
    # 合并为一个图
    combined_chart = (price_line + event_lines + event_labels).properties(
        width=800,
        height=400,
        title=f"{selected_code} 收盘价 + 公告事件"
    ).add_selection(
        brush
    )
    
    # 展示图表
    st.altair_chart(combined_chart, use_container_width=True)


