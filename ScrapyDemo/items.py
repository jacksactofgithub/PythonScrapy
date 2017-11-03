# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
定义scrapy工程中使用的实体类
"""

class ScrapydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class mPhoneItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()

class CourseItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    introduction = scrapy.Field()
    student = scrapy.Field()

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url =scrapy.Field()
    create_date = scrapy.Field()
    img_url = scrapy.Field()