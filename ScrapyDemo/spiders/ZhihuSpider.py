
import scrapy
# from scrapy.http import FormRequest
#import time
import os
import json
from PIL import Image


class ZhihuSpider(scrapy.spiders.Spider):
    name = "ZhihuSpider"
    """
    def start_requests(self):
        return[
            FormRequest(
                "https://www.zhihu.com/",
                formdata={"_xsrf":"33323565666564622d353939342d346139312d383631652d316239303639643166343733",
                          "password": "ls1995429",
                          "captcha_type":"cn",
                          "email":"2653909025@qq.com"
                          }
            )
        ]
    """
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/']
    Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'

    header = {
        'User-Agent': Agent,
    }

    def parse(self, response):
        # 主页爬取的具体内容
        pass

    def start_requests(self):
        #t = str(int(time.time() * 1001))
        # 知乎登录验证码获取地址 从请求验证码开始知乎为爬虫请求生成一个session 用户请求的验证码放到session中(猜测)
        #captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=en'
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=15000778515&type=login&lang=en'
        return [scrapy.Request(url=captcha_url, headers=self.header, callback=self.parser_captcha)]

    def parser_captcha(self, response):
        with open(r"C:\Users\Jack\Desktop\captcha.jpg", 'wb') as f:
            f.write(response.body)
            f.close()
        try:
            im = Image.open(r"C:\Users\Jack\Desktop\captcha.jpg")
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        #将获取到的验证码放到meta中
        return scrapy.FormRequest(url='https://www.zhihu.com/#signin', headers=self.header,callback=self.login, meta={'captcha': captcha})

    def login(self, response):
        xsrf = response.xpath("//input[@name='_xsrf']/@value").extract_first()
        if xsrf is None:
            return ''
        post_url = 'https://www.zhihu.com/login/email'
        post_data = {
            "_xsrf": xsrf,
            "email": '2653909025@qq.com',
            "password": 'ls1995429',
            "captcha": response.meta['captcha']
        }
        return [scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.header, callback=self.check_login)]

    # 验证返回是否成功
    def check_login(self, response):
        js = json.loads(response.text)
        if 'msg' in js and js['msg'] == '登录成功':
            print("登录成功")
            for url in self.start_urls:
                yield scrapy.Request(url=url, headers=self.header, dont_filter=True)
        else:
            print("登录失败")


"""
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36
"""