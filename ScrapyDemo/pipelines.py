# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ScrapydemoPipeline(object):
    def process_item(self, item, spider):
        return item

class MoocSpiderPipeline(object):
    def __init__(self):#__init__方法在类被实例化的时候自动调用，用于初始化对象
        self.file = open('F:\data.json','w',encoding='utf-8')
        print("pipeline init")

    def process_item(self,item,spider):
        #dumps将dict转换为str格式 dict(item)将item转换为dict类型
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        print(type(dict(item)))
        #写入文件
        self.file.write(line)
        return item
    #spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #spider被关闭时被调用
    def close_spider(self, spider):
        pass

class MysqlPipilin(object):
    def __init__(self):
        self.conn =pymysql.connect(host='192.168.1.19',port=3306,user='root',passwd='123456',db='article_spider',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()
