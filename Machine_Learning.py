import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.title("📈 基于机器学习的股票上涨预测")
st.markdown("""
### 🧠 机器学习模型说明

我们使用了 **随机森林分类器（Random Forest）** 来学习每支股票的近期走势模式，并预测**下一日是否上涨**：

| 特征名称       | 描述 |
|----------------|------|
| 开盘价、收盘价 | 当日价格信息 |
| 5日均价        | 收盘价5日滑动平均，衡量趋势 |
| 成交量         | 市场活跃度 |
| 5日成交量均值  | 近期平均成交量 |
| 是否阳线       | 当日是否为阳线 |
| 振幅           | 当日价格波动幅度 |

**上涨概率越高**，说明模型认为该股票第二天上涨的可能性越大。
""")

uploaded_file = st.file_uploader("上传股票历史数据 CSV（多只股票）", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values(['股票代码', '日期'])

    # 构造标签：明日涨跌幅 > 0 为上涨
    df['明日收盘价'] = df.groupby('股票代码')['收盘价'].shift(-1)
    df['涨跌幅'] = (df['明日收盘价'] - df['收盘价']) / df['收盘价']
    df['label'] = (df['涨跌幅'] > 0).astype(int)

    # 构造特征
    df['5日均价'] = df.groupby('股票代码')['收盘价'].transform(lambda x: x.rolling(5).mean())
    df['5日成交量均值'] = df.groupby('股票代码')['成交量'].transform(lambda x: x.rolling(5).mean())
    df['是否阳线'] = (df['收盘价'] > df['开盘价']).astype(int)
    df['振幅'] = df['振幅']

    features = ['开盘价', '收盘价', '5日均价', '成交量', '5日成交量均值', '是否阳线', '振幅']
    df = df.dropna(subset=features + ['label'])  # 去除缺失值

    # 拆分数据集
    X = df[features]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 模型训练
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 预测所有最新一日的每支股票
    latest_rows = df.groupby('股票代码').tail(1).copy()
    latest_rows['上涨概率'] = model.predict_proba(latest_rows[features])[:, 1]

    st.subheader("📊 预测结果（上涨概率）")
    st.dataframe(latest_rows[['股票代码', '日期', '上涨概率']].sort_values('上涨概率', ascending=False))

    # 下载
    result = latest_rows[['股票代码', '日期', '上涨概率']].sort_values('上涨概率', ascending=False)
    csv = result.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 下载预测结果 CSV", data=csv, file_name='predicted_up_stocks.csv')
