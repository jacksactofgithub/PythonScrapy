__author__ = 'liushuo'
import scrapy
from scrapy.http import FormRequest
import json
from PIL import Image
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from urllib.parse import urlencode
import urllib

class ZhihuSpider(scrapy.spiders.Spider):
    name = "ZhihuSpider"
    allowed_domains = ['www.zhihu.labs']
    start_urls = ['https:/www.zhihu.labs/api/v4/questions/37709992/answers?']#长得好看但是没有男朋友
    Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
    header = {
        'User-Agent': Agent,
    }
    index = 0

    def start_requests(self):
        # 知乎登录验证码获取地址 从请求验证码开始知乎为爬虫请求生成一个session 用户请求的验证码放到session中(猜测)
        captcha_url = 'https://www.zhihu.labs/captcha.gif?r=15000778515&type=login&lang=en'
        return [scrapy.Request(url=captcha_url, headers=self.header, callback=self.parser_captcha)]

    def parser_captcha(self, response):
        with open(r"E:\pythondl\captcha.jpg", 'wb') as f:
            f.write(response.body)
            f.close()

        im = Image.open(r"E:\pythondl\captcha.jpg")
        im.show()
        im.close()
        #从控制台手动输入验证码
        captcha = input("请输入图中的验证码\n>")
        #请求知乎登录页面#signin;获取将获取到的验证码放到meta中
        return scrapy.FormRequest(url='https://www.zhihu.labs/#signin', headers=self.header,callback=self.login,
                                  meta={'captcha': captcha})

    def login(self, response):
        #登录页面body中有登录表单需要提交的_xsrf参数的值,用xpath解析response得到_xsrf的值
        xsrf = response.xpath("//input[@name='_xsrf']/@value").extract_first()
        if xsrf is None:
            return ''
        #登录表单的post地址,captcha为上一步请求到的验证码的值;服务器端在爬虫请求验证码的时候把验证码存储在session中,爬虫post登录
        #时比较提交的表单中的验证码值和session中的值是否相等
        post_url = 'https://www.zhihu.labs/login/email'
        post_data = {
            "_xsrf": xsrf,
            "email": '2653909025@qq.labs',
            "password": 'ls1995429',
            "captcha": response.meta['captcha']
        }
        return [FormRequest(url=post_url, formdata=post_data, headers=self.header, callback=self.parse)]

    # 验证返回是否成功
    def check_login(self,response):
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
                for i in range(0,20):
                    form_data={
                        'include':('data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,'
                                  'annotation_action,annotation_detail,collapse_reason,is_sticky,'
                                  'collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,'
                                  'voteup_count,reshipment_settings,comment_permission,created_time,updated_time,'
                                  'review_info,question,excerpt,relationship.is_authorized,is_author,voting,'
                                  'is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;'
                                  'data[*].author.follower_count,badge[?(type=best_answerer)].topics'),
                        'limit':str(20),
                        'offset':str(3 + 20 * i),
                        'sort_by':'default'
                    }
                    data = str(urlencode(form_data).encode('utf-8'))
                    #yield scrapy.Request(url=url+data, headers=self.header, method='GET', callback=self.downloadImg)
                    #yield scrapy.Request(url=url,headers=self.header, callback=self.downloadImg)

                    req = urllib.request.Request(url,data,self.header,method='GET')
                    res = urllib.request.urlopen(req)


    def downloadImg(self,response):
        js = json.loads(response.text)
        print(js['paging']['totals'])
        """
        images = response.xpath('//img[@class="origin_image zh-lightbox-thumb lazy"]/@data-actualsrc').extract()
        i=1
        for img in images:
            request.urlretrieve(img,'E:\pythondl\%dpic%s.jpg' % (self.index,i))
            i+=i
        self.index+=1
        """

    def FReqErrback(self,failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

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
#include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics