import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
from io import StringIO

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

# Streamlit应用界面
st.set_page_config(layout="wide")
st.title('📈 股票资金流向分析工具')

# 文件上传区域
uploaded_file = st.file_uploader("上传资金流向CSV文件", type="csv")

if uploaded_file is not None:
    # 读取数据
    stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
    df = pd.read_csv(stringio)
    
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
