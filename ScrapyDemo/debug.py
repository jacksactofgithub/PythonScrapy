__author__ = 'liushuo'
from scrapy.cmdline import execute
#from scrapy import cmdline
#命令行运行scrapy库相当于运行此命令;run configuration中配置script params为crawl spidername
cmd = 'scrapy crawl ZhihuSpider'
execute()