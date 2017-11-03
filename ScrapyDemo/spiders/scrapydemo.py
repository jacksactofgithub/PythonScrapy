__author__ = 'liushuo'
import scrapy
#from scrapy.selector import Selector
#from scrapy.http import HtmlResponse

class scrapydemo(scrapy.spiders.Spider):
    name = "scrapydemo"#必须定义name
    start_urls = ["https://list.jd.com/list.html?cat=9987,653,655"]#定义要抓取的网页url 京东手机分类

    def parse(self,response):#必须实现parse方法 scrapy源码中默认callback函数的函数名
        """
        current_url = response.url #回调时爬取的url
        body = response.body #返回的html
        unicode_body = response.body_as_unicode()#返回的html unicode编码

        num_pages = int(response.xpath('//div[contains(@class, "p-name")]/text()').extract_first())
        base_url = "http://www.allitebooks.com/security/page/{0}/"
        for page in range(1, num_pages):
            yield scrapy.Request(base_url.format(page), dont_filter=True, callback=self.parse_page)
        for i in range(len(phonenames)):
            print(phonenames[i])
        """
        #筛选div标签中 属性class=p-name 的<a>/<em>字节点的元素值
        phonenames = response.xpath('//div[@class="p-name"]/a/em/text()').extract()
        shopnames = response.xpath('//div[@class="p-shop"]/@data-shop_name').extract()
        for (phonename,shopname)in zip(phonenames,shopnames):
            print(phonename.lstrip())#去掉前后空格
            print(shopname)
