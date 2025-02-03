from data_collection.spider import SimpleSpider

simplespider = SimpleSpider()
data_example = simplespider.scrape_website("https://www.cls.cn/")

print(data_example)


