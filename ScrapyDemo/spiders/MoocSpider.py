__author__ = 'liushuo'
import scrapy
from ScrapyDemo.items import CourseItem

class MoocSpider(scrapy.spiders.Spider):
    name = "MoocSpider"
    start_urls = ["http://www.imooc.com/course/list"]

    def parse(self,response):
        item = CourseItem()
        boxs = response.xpath('//div[@class="course-card-container"]/a[@target="_blank"]')
        print(type(boxs))
        for box in boxs:
            #对每个课程的box解析 得到课程标题简介等信息
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            item['image_url'] = 'http'+box.xpath('.//@src').extract()[0]
            item['title'] = box.xpath('.//h3[@class="course-card-name"]/text()').extract()[0].strip()
            item['student'] = box.xpath('.//div[@class = "course-card-info"]/span/text()').extract()[1].strip()#[:-3]
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            """
            yield关键词,作用是返回一个对象(parse会调用pipelines处理)后继续执行以实现递归处理
            使用了yield parse函数会被当做一个生成器使用.scrapy会逐一获取parse方法中生成的结果 并判断结果是什么样的类型
            如果是request则加入爬取队列,如果是item类型则使用pipeline处理,其他类型返回错误信息
            """
            yield item