import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from fake_useragent import UserAgent
from urllib.parse import urljoin
import time

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
        print("文本内容:")
        print(text_content)
        
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
        
        return json.dumps(data, ensure_ascii=False, indent=4)

# 示例用法
if __name__ == "__main__":
    spider = SimpleSpider()
    url = 'https://www.cls.cn/'  # 替换为目标网站
    result = spider.scrape_website(url)
    print(result)
    time.sleep(1)  # 增加延迟，避免频繁请求
