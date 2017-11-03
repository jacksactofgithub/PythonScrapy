__author__ = 'liushuo'
import scrapy
from scrapy.http import Request
from ScrapyDemo.items import ArticleItem

class WebPageSpider(scrapy.spiders.Spider):
    name = "WebPageSpider"
    start_urls = ["http://blog.jobbole.com/all-posts/"]

    def parse(self,response):
        articles = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]')
        for article in articles:
            title = article.xpath('./a/@title').extract_first()
            articlePath  = article.xpath('./a/@href').extract_first()
            imgUrl= article.xpath('./a/img/@src').extract_first()
            yield Request(url=articlePath,meta={"imgurl":imgUrl},callback=self.parseArticle)

        #如果有下一页循环调用parse抓取
        nextUrl = response.xpath('//div[@class="navigation.margin-20"]/a[@class="next page-numbers"]/@href').extract_first()
        if nextUrl:
            yield Request(url=nextUrl,callback=self.parse())

    """
    parse方法中的scrapy request对象执行了对参数中url的请求并由downloader执行后产生一个response传递给callback参数中指定的函数
    """
    def parseArticle(self,response):
        articleItem = ArticleItem()
        url = response.url
        img_url = response.meta.get("imgurl")
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().split()[0]
        articleItem["title"] = title
        articleItem["url"] = url
        articleItem["create_date"] = create_date
        articleItem["img_url"] = img_url
        yield articleItem




