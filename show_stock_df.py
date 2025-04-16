

import streamlit as st
from data_collection.spider import FundFlowScraper

st.title("🧊 股票详情数据爬虫")

scraper = FundFlowScraper(page_size=50)
df = scraper.scrape_all()

st.dataframe(df)

csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button("下载 CSV", csv, "资金流.csv", "text/csv", key='download-csv')
