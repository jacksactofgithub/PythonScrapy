__author__ = 'liushuo'
import scrapy
from scrapy.http import FormRequest
import os
import json
from PIL import Image
from urllib import request


class ZhihuSpider(scrapy.spiders.Spider):
    name = "ZhihuSpider"
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/37709992']#长得好看但是没有男朋友
    Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
    header = {
        'User-Agent': Agent,
    }


    def start_requests(self):
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
        #从控制台手动输入验证码
        captcha = input("please input the captcha\n>")
        #请求知乎登录页面#signin;获取将获取到的验证码放到meta中
        return scrapy.FormRequest(url='https://www.zhihu.com/#signin', headers=self.header,callback=self.login,
                                  meta={'captcha': captcha})

    def login(self, response):
        #登录页面body中有登录表单需要提交的_xsrf参数的值,用xpath解析response得到_xsrf的值
        xsrf = response.xpath("//input[@name='_xsrf']/@value").extract_first()
        if xsrf is None:
            return ''
        #登录表单的post地址,captcha为上一步请求到的验证码的值;服务器端在爬虫请求验证码的时候把验证码存储在session中,爬虫post登录
        #时比较提交的表单中的验证码值和session中的值是否相等
        post_url = 'https://www.zhihu.com/login/email'
        post_data = {
            "_xsrf": xsrf,
            "email": '2653909025@qq.com',
            "password": 'ls1995429',
            "captcha": response.meta['captcha']
        }
        return [FormRequest(url=post_url, formdata=post_data, headers=self.header, callback=self.parse)]

    # 验证返回是否成功
    def check_login(self, response):
        js = json.loads(response.text)
        if 'msg' in js and js['msg'] == '登录成功':
            print(js['msg'])
            return True
        else:
            print(js['msg'])
            return False

    def parse(self, response):
        # 首先检查是否登录成功,登录成功后请求目标url并缴费downloadImg函数处理
        if self.check_login(response):
            for url in self.start_urls:
                for i in range[20]:
                    data={}
                    data['sort_by'] = 'default'
                    data['include'] = 'data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,' \
                                      'can_comment,content,editable_content,voteup_count,reshipment_settings,' \
                                      'comment_permission,mark_infos,created_time,updated_time,' \
                                      'relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,' \
                                      'upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'
                    data['limit'] = 20
                    data['offset'] = 3 + 20 * i
                    yield scrapy.Request(url=url, headers=self.header, data=data, meta={"index":i},
                                         dont_filter=True, callback=self.downloadImg)

    def downloadImg(self,response):
        images = response.xpath('//img[@class="origin_image zh-lightbox-thumb lazy"]/@data-actualsrc').extract()
        i=1
        for img in images:
            request.urlretrieve(img,'E:\pythondl\%dpic%s.jpg' % (response.meta['index'],i))
            i+=i
        pass


"""
知乎登录的form表单
_xsrf:33323565666564622d353939342d346139312d383631652d316239303639643166343733
password:**********
captcha_type:en
email:*************

登录请求的response
data:{password: "请输入 6-128 位的密码"}
password:"请输入 6-128 位的密码"
errcode:100004
msg:"请输入 6-128 位的密码"
r:1

明日todo:设置登录cookie; 抓取知乎问题下的所有回答
http://blog.csdn.net/github_38196368/article/details/72755669
"""