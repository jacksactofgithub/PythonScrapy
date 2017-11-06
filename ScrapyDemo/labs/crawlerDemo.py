from ctypes import WinError

__author__ = 'liushuo'
import urllib.request
import urllib
import re
import socket
import time


def  getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} #添加useragent信息
    page = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(page).read()

    # page = urllib.request.urlopen(url)
    # html = page.read()
    return html

def getImg(html):
    reg = r'src="(.*?\.jpg)"'    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    x = 0
    timeout = 20
    socket.setdefaulttimeout(timeout)  # 这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
    sleep_download_time = 10

    for imgurl in imglist:
        imgurl = "http://91.p9b.space/"+imgurl.split("file=\"")[1]
        print(imgurl)

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(imgurl,'E:\pythondl\%s.jpg' % x)
        except WinError:
            sleep_download_time += 10
            print("error occur")

        time.sleep(sleep_download_time)  # 这里时间自己设定
        #request.close()  # 记得要关闭

        urllib.request.urlretrieve(imgurl,'E:\pythondl\%s.jpg' % x)
        x+=1

def getVerf(verfurl):
    #imgurl = "https://www.zhihu.com/captcha.gif?r=1509881621577&type=login&lang=en"
    for i in range(20):
        urllib.request.urlretrieve(verfurl,'E:\pythondl\%s.jpg' % i)
        i+=i


# data = getHtml("http://91.p9b.space/viewthread.php?tid=194745&extra=page%3D10")
# data = data.decode('utf-8')
# getImg(data)

getVerf("https://www.zhihu.labs/captcha.gif?r=1509881621577&type=login&lang=cn")