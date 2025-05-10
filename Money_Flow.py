import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams

matplotlib.rc("font",family='MicroSoft YaHei',weight="bold")
# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def plot_money_flow(data):
    """绘制资金流向对比图"""
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 左轴：收盘价
    color = 'tab:red'
    ax1.set_xlabel('日期')
    ax1.set_ylabel('收盘价（元）', color=color)
    line_close, = ax1.plot(data['日期'], data['收盘价'], color=color, marker='o', label='收盘价')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    
    # 右轴：资金流向（万元）
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('资金净流入（万元）', color=color)
    
    # 绘制各资金类型曲线
    funds = {
        '主力': data['主力净流入(元)']/10000,
        '大单': data['大单净流入(元)']/10000,
        '超大单': data['超大单净流入(元)']/10000,
        '中单': data['中单净流入(元)']/10000,
        '小单': data['小单净流入(元)']/10000
    }
    
    lines = [line_close]
    for name, values in funds.items():
        line, = ax2.plot(data['日期'], values, marker='.', label=name)
        lines.append(line)
    
    ax2.axhline(0, color='gray', linestyle=':', linewidth=0.8)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 合并图例
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper left', bbox_to_anchor=(1.1, 1))
    
    # 标题和格式
    stock_name = data['股票名称'].iloc[0] if '股票名称' in data.columns else ''
    plt.title(f'{stock_name} 价格与资金流向对比', pad=20)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


import altair as alt

def plot_money_flow_streamlit(data):
    """使用Streamlit和Altair绘制资金流向对比图，支持双Y轴和中文显示"""
    
    # 数据预处理
    df_viz = data.copy()
    df_viz['日期'] = pd.to_datetime(df_viz['日期'])
    df_viz.set_index('日期', inplace=True)
    
    # 转换为万元单位
    for col in ['主力净流入(元)', '大单净流入(元)', '超大单净流入(元)', '中单净流入(元)', '小单净流入(元)']:
        df_viz[col] = df_viz[col] / 10000
    
    # 重置索引以便 Altair 使用日期列
    df_viz = df_viz.reset_index()
    
    # 创建图表标题
    st.subheader(f"{df_viz['股票名称'].iloc[0]} 价格与资金流向对比")
    
    # 选项卡布局
    tab1, tab2 = st.tabs(["📈 趋势对比", "🧮 资金分解"])
    
    with tab1:
        # 主图表 - 价格与主力资金（类似双Y轴）
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.markdown("**收盘价 vs 主力资金**")
            
            # Altair 图表：收盘价
            price_chart = alt.Chart(df_viz).mark_line(color='red').encode(
                x=alt.X('日期:T', title='日期'),
                y=alt.Y('收盘价:Q', title='收盘价 (元)', scale=alt.Scale(zero=False)),
                tooltip=['日期', '收盘价']
            ).properties(
                width=600,
                height=400
            )
            
            # Altair 图表：主力净流入
            fund_chart = alt.Chart(df_viz).mark_line(color='blue').encode(
                x=alt.X('日期:T', title='日期'),
                y=alt.Y('主力净流入(元):Q', title='主力净流入 (万元)', scale=alt.Scale(zero=False)),
                tooltip=['日期', '主力净流入(元)']
            ).properties(
                width=600,
                height=400
            )
            
            # 合并图表，使用 resolve_scale 实现独立Y轴
            combined_chart = alt.layer(price_chart, fund_chart).resolve_scale(
                y='independent'  # 使Y轴独立
            ).configure(
                font='SimHei'  # 设置中文字体（需确保系统有该字体）
            ).configure_axis(
                titleFont='SimHei',
                labelFont='SimHei'
            )
            
            # 显示 Altair 图表
            st.altair_chart(combined_chart, use_container_width=True)
        
        with col2:
            st.metric("累计主力净流入", f"{df_viz['主力净流入(元)'].sum():.1f}万元")
            st.metric("平均收盘价", f"{df_viz['收盘价'].mean():.2f}元")
    
    with tab2:
        # 资金流向堆叠面积图（保持原样）
        st.markdown("**资金流向分解（万元）**")
        st.area_chart(
            df_viz.set_index('日期')[['超大单净流入(元)', '大单净流入(元)', '中单净流入(元)', '小单净流入(元)']],
            color=['#32CD32', '#FFA500', '#BA55D3', '#FF4500']  # 超大单绿, 大单橙, 中单紫, 小单红
        )
    
    # 添加交互控件
    with st.expander("⚙️ 图表配置"):
        date_range = st.date_input(
            "选择日期范围",
            value=[df_viz['日期'].min(), df_viz['日期'].max()],
            min_value=df_viz['日期'].min(),
            max_value=df_viz['日期'].max()
        )
        
        selected_funds = st.multiselect(
            "选择要显示的资金类型",
            options=['主力', '大单', '超大单', '中单', '小单'],
            default=['主力', '超大单']
        )
        
        # 应用筛选
        filtered_df = df_viz[(df_viz['日期'] >= pd.to_datetime(date_range[0])) & 
                            (df_viz['日期'] <= pd.to_datetime(date_range[1]))]
        fund_cols = [f'{x}净流入(元)' for x in selected_funds]
        
        if selected_funds:
            # Altair 交互图表
            price_chart = alt.Chart(filtered_df).mark_line(color='red').encode(
                x=alt.X('日期:T', title='日期'),
                y=alt.Y('收盘价:Q', title='收盘价 (元)', scale=alt.Scale(zero=False)),
                tooltip=['日期', '收盘价']
            )
            
            # 动态添加资金流向线
            fund_charts = []
            colors = ['#4169E1', '#32CD32', '#FFA500', '#BA55D3', '#FF4500']
            for i, col in enumerate(fund_cols):
                fund_chart = alt.Chart(filtered_df).mark_line(color=colors[i]).encode(
                    x=alt.X('日期:T', title='日期'),
                    y=alt.Y(f'{col}:Q', title='资金净流入 (万元)', scale=alt.Scale(zero=False)),
                    tooltip=['日期', col]
                )
                fund_charts.append(fund_chart)
            
            # 合并所有图表
            combined_chart = alt.layer(price_chart, *fund_charts).resolve_scale(
                y='independent'  # 独立Y轴
            ).configure(
                font='SimHei'
            ).configure_axis(
                titleFont='SimHei',
                labelFont='SimHei'
            )
            
            st.altair_chart(combined_chart, use_container_width=True)

# Streamlit应用界面
st.set_page_config(layout="wide")
st.title('📈 股票资金流向分析工具')

# 文件上传区域
uploaded_file = st.file_uploader("上传资金流向CSV文件", type="csv")

if uploaded_file is not None:
    # 读取数据
    df = pd.read_csv(uploaded_file, dtype={'代码': str})
    
    # 数据预处理
    numeric_cols = [col for col in df.columns if col not in ['日期', '股票代码', '股票名称']]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # 显示原始数据
    st.subheader('📋 原始数据预览')
    st.dataframe(df.head())
    
    # 选择分析的股票（如果文件包含多只股票）
    if '股票代码' in df.columns:
        selected_stock = st.selectbox('选择要分析的股票', df['股票名称'].unique())
        df = df[df['股票名称'] == selected_stock]
    
    # 绘制图表
    st.subheader('📊 价格与资金流向对比')
    fig = plot_money_flow(df)
    
    st.pyplot(fig)
    
    # 资金分析指标
    st.subheader('🧮 资金分析')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("主力净流入总额", f"{df['主力净流入(元)'].sum()/10000:,.1f}万元")
        
    with col2:
        st.metric("大单净流入总额", f"{df['大单净流入(元)'].sum()/10000:,.1f}万元")
        
    with col3:
        st.metric("超大单净流入总额", f"{df['超大单净流入(元)'].sum()/10000:,.1f}万元")
    
    # 下载按钮
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载分析数据",
        data=csv,
        file_name='资金流向分析.csv',
        mime='text/csv'
    )

    plot_money_flow_streamlit(df)

else:
    st.info('请上传CSV文件，格式参考：日期,主力净流入(元),小单净流入(元),中单净流入(元),大单净流入(元),超大单净流入(元)...')

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 上传标准格式的CSV文件
2. 系统自动解析数据并生成可视化
3. 可下载分析结果

### 文件格式要求
- 必须包含日期、收盘价和各资金流向列
- 支持多股票数据（自动筛选）
""")
