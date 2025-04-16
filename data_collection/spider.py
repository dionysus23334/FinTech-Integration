import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from fake_useragent import UserAgent
from urllib.parse import urljoin
import time
from selenium import webdriver

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

class SeleniumAutoSpider:

    def __init__(self):
        # 启动浏览器（可设置为无头）
        # streamlit 线上部署没有Edge要用Chrome
        # self.driver = webdriver.Edge()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # 访问目标网站
        url = 'https://data.eastmoney.com/zjlx/list.html'
        self.driver.get(url)
        # 等待某个关键元素出现，说明数据已加载（例如等“涨幅”字段不再是“-”）
        time.sleep(5)
        # 提取表格 HTML
        html = self.driver.page_source
        # 用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, "html.parser")
        # 找到 class 为 dataview-body 的容器
        container = soup.find("div", class_="dataview-body")
        # 在其中找 table 标签
        table = container.find("table")
        stock_data = {}
        for row in table.find_all('tr')[2:]:  # 前两行为表头
            cells = row.find_all('td')
            if len(cells) < 15:
                continue
            
            stock_code = cells[1].get_text(strip=True)
        
        
            for cell in cells:
                a = cell.find('a')
                if a and a.get('href'):
                    data = {}
                    text = a.get_text(strip=True)
                    href = a['href']
                    if text == '详情':
                        data[text] = "https://data.eastmoney.com" + href       
                        break  
        
            stock_data[stock_code] = {
                "序号": cells[0].get_text(strip=True),
                "代码": stock_code,
                "名称": cells[2].get_text(strip=True),
                "相关资讯": data,
                "最新价": cells[4].get_text(strip=True),
                "今日主力净占比": cells[5].get_text(strip=True),
                "今日排名": cells[6].get_text(strip=True),
                "今日涨跌": cells[7].get_text(strip=True),
                "5日主力净占比": cells[8].get_text(strip=True),
                "5日排名": cells[9].get_text(strip=True),
                "5日涨跌": cells[10].get_text(strip=True),
                "10日主力净占比": cells[11].get_text(strip=True),
                "10日排名": cells[12].get_text(strip=True),
                "10日涨跌": cells[13].get_text(strip=True),
                "所属板块": cells[14].get_text(strip=True),
            }
        self.stock_data = stock_data

    def get_dataframe(self):

        self.stock_data = pd.DataFrame(self.stock_data).T
        
        return self.stock_data


# 示例用法
if __name__ == "__main__":
    spider = SimpleSpider()
    url = 'https://www.cls.cn/'  # 替换为目标网站
    result = spider.scrape_website(url)
    print(result)
    time.sleep(1)  # 增加延迟，避免频繁请求
