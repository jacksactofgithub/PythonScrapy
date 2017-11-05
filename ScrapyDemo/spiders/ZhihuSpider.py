import scrapy
from scrapy.http import FormRequest

class ZhihuSpider(scrapy.spiders.Spider):
    name ="ZhihuSpider"
    start_urls=[""]

    def parse(self):
        pass
