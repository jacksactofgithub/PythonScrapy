# -*- coding: utf-8 -*-
import scrapy
from ScrapyDemo.items import TwoColorItem


class TwoColorSpider(scrapy.Spider):
    # 用于区别Spider
    name = "TwoColorSpider"
    # 允许访问的域
    allowed_domains = ["caipiao.163.com"]
    # 爬取的地址
    start_urls = ["http://trend.caipiao.163.com/ssq/?beginPeriod=2004001&endPeriod=2017137"]

    # 爬取方法
    def parse(self, response):

        whole = response.xpath("//tbody[@id='cpdata']")

        for tr in whole.xpath("//tr[@data-period]"):

            item = TwoColorItem()

            print()

            item.date = tr.xpath("./tr/@date-period").extract_first()

            for td in tr.xpath("//td[@class]"):

                classOfTd = td.xpath("@class")

                if classOfTd == "ball_brown" or classOfTd == "ball_red":
                    item.red = item.red + "_" + "0"

                if classOfTd == "f_red":
                    item.red = item.red + "_" + td.xpath("text()").extract_first()

                if classOfTd == "f_blue":
                    item.blue = item.blue + "_" + td.xpath("text()").extract_first()

                if classOfTd == "ball_blue js-fold":
                    item.blue = item.blue + "_" + "0"

            print(item.date + "  red:" + item.red + "  blue:" + item.blue)
