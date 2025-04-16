import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from fake_useragent import UserAgent
from urllib.parse import urljoin
import time
from selenium import webdriver
import math

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



class SimpleSpider:

    def __init__(self):
        # 初始化随机 User-Agent
        self.ua = UserAgent()

    def get_random_headers(self):
        # 生成随机请求头
        return {
            'User-Agent': self.ua.random
        }

    def scrape_website(self, url):
        # 发送 HTTP 请求
        headers = self.get_random_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取所有文本内容
        text_content = soup.get_text()
        
        # Extract all links from <a> tags
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Extract all images from <img> tags
        image_links = [img['src'] for img in soup.find_all('img', src=True)]

        # 提取表格数据
        tables = soup.find_all('table')
        tables_data = []
        
        for table in tables:
            try:
                # 使用 pandas 提取表格数据
                df = pd.read_html(str(table))[0]  # 获取第一个表格
                tables_data.append(df.to_dict(orient='records'))  # 转换为字典列表
            except Exception as e:
                print(f"表格解析失败: {e}")

        # 构建 JSON 结构
        data = {
            'text': text_content,
            'links': links,
            'images': image_links,
            'tables': tables_data
        }
        
        return data

# fundflow_scraper.py


class FundFlowScraper:
    def __init__(self, page_size=50, sleep_sec=0.5):
        self.ua = UserAgent()
        self.page_size = page_size
        self.sleep_sec = sleep_sec
        self.base_url = "https://push2.eastmoney.com/api/qt/clist/get"
        self.params = {
            "fid": "f184",
            "po": "1",
            "pz": str(page_size),
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
            "fs": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
            "fields": "f2,f3,f12,f14,f62,f184,f225,f109,f160,f124,f100,f1"
        }
        self.headers = {
            "User-Agent": self.ua.random,
            "Referer": "https://data.eastmoney.com/zjlx/list.html"
        }
        self.field_map = {
            "f2": "最新价",
            "f3": "涨跌幅",
            "f12": "股票代码",
            "f14": "股票名称",
            "f62": "主力净流入",
            "f184": "主力净占比",
            "f225": "超大单净流入",
            "f109": "所属板块",
            "f160": "涨速",
            "f124": "量比",
            "f100": "换手率",
            "f1": "序号"
        }

    def _get_total_pages(self):
        res = requests.get(self.base_url, params=self.params, headers=self.headers)
        res_json = res.json()
        total = res_json['data']['total']
        pages = math.ceil(total / self.page_size)
        return total, pages

    def scrape_all(self):
        total, pages = self._get_total_pages()
        print(f"共 {total} 条数据，{pages} 页，每页 {self.page_size} 条")
        all_data = []

        for page in range(1, pages + 1):
            print(f"抓取第 {page} 页...")
            self.params['pn'] = str(page)
            res = requests.get(self.base_url, params=self.params, headers=self.headers)
            res_json = res.json()
            data = res_json['data']['diff']
            all_data.extend(data)
            time.sleep(self.sleep_sec)

        df = pd.DataFrame(all_data)
        df = df.rename(columns=self.field_map)
        return df

    def save_csv(self, df: pd.DataFrame, filename="资金流.csv"):
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到 {filename}")



# 示例用法
if __name__ == "__main__":
    spider = SimpleSpider()
    url = 'https://www.cls.cn/'  # 替换为目标网站
    result = spider.scrape_website(url)
    print(result)
    time.sleep(1)  # 增加延迟，避免频繁请求
