import streamlit as st

st.html(
    
    """
    <p style='font-weight:bold;; font-size:50px; text-align:center;'>FinTech Application</p>
    <p style='font-size:25px; color:grey; text-align:center;'>Author: Yuxi Guo</p>
    """
    )

st.write(
    '''
    Through the collaboration on spider, quantization and prompt engineering, 
    this project proposes a system for financial information analysis and market prediction.
    User can apply the various data on websites or input the keyword.
    '''
)
st.markdown("""
# 📊 欢迎使用多功能数据分析平台！

本平台集成了多个数据处理与分析模块，支持聊天机器人、自然语言处理、股票分析等多个应用场景。以下是当前可用功能模块：

---

## 🏠 Home
> 平台首页，展示功能概览与入口导航。

---

## 🤖 Chatbot
> 与智能聊天机器人互动，支持问答、闲聊和任务指令。

---

## 📚 NLP Analysis
> 分析文本情感、关键词提取、词云生成等自然语言处理功能。

---

## 💹 Stock Data
> 浏览和处理股票K线数据，支持上传、自定义排序与筛选。

---

## 🔢 RPS And STD
> 根据股票收益率评分（RPS）与标准差分析波动性，辅助股票筛选。

---

## 📅 Events And Prices
> 事件驱动分析模块，查看事件与股价在时间轴上的联动。

---

## 📈 Momentum App
> 基于动量策略构建投资组合，支持选股、回测和可视化。

---

## 📐 Average Lines
> 查看多只股票的5日、10日、20日均线，支持上传数据与可视化选择。

---
> 💡 请从左侧侧边栏选择模块开始使用~
""")
