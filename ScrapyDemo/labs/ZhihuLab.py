__author__ = 'liushuo'

import urllib.request
import json
import urllib.parse
import re
import random
n=0
for i in range(0,10):
    url='https://www.zhihu.com/api/v4/questions/37709992/answers?'
    data={}
    head={}
    #head为请求头部封装
    head['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
    head['accept']='application/json, text/plain, */*'
    # head['Accept-Encoding']='utf-8, deflate, sdch, br'
    head['Accept-Language']='zh-CN,zh;q=0.8'
    head['Referer']='https://www.zhihu.com/question/37709992'
    #head['authorization']='Bearer Mi4xa2pBbkFBQUFBQUFBTUVKbWhHblhDeGNBQUFCaEFsVk56eUhnV2dEQnBGUEV0Y0VrbEpCMVdPSzFHalFEUkN5Qy1n|1509086159|948dd2dc563b900e5ed47b557f0709cb897cdab4'
    head['Connection']='keep-alive'
    head['host']='www.zhihu.com'
    head['Cookie']='aliyungf_tc=AQAAALVd9EriDg0AvpVAcEvWZbUkeHws; acw_tc=AQAAAFgY4CTawQ0AvpVAcIyKPeu+gUqo; ' \
                   'd_c0="ADBCZoRp1wuPTsifoRjfVfZV8xEatgY8_lY=|1496214627"; _zap=1481caa5-a617-485b-a7bd-d78a47dbd112; ' \
                   'q_c1=ed4e718e03e746d4824f12b4bed18c73|1508480132000|1493023322000; ' \
                   'r_cap_id="M2ZmMzM4OTU5NmNjNGI3YmEzNWFiMjVmNTcyMDM4MGI=|1509086151|968f257094662aaa20c829956e9a6c99a7cbec71"; ' \
                   'cap_id="ZTMzMTExNmJmOTYxNDJjZDkxOWVjNGY0NjI1MGJlNzU=|1509086151|83e816a29369ec0e5f8b91d97f9e112da7be9383"; ' \
                   'z_c0=Mi4xa2pBbkFBQUFBQUFBTUVKbWhHblhDeGNBQUFCaEFsVk56eUhnV2dEQnBGUEV0Y0VrbEpCMVdPSzFHalFEUkN5Qy1n|1509086159|' \
                   '948dd2dc563b900e5ed47b557f0709cb897cdab4; q_c1=ed4e718e03e746d4824f12b4bed18c73|1509418825000|1493023322000; ' \
                   '__utma=51854390.1663933463.1496214628.1509934701.1509943982.29; __utmc=51854390; ' \
                   '__utmz=51854390.1509943982.29.22.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/27985322; ' \
                   '__utmv=51854390.100-1|2=registration_date=20131209=1^3=entry_date=20131209=1;' \
                   ' _xsrf=3cca64a7f18fb7e30018a0a0240f3182'

    #data为数据部分
    data['sort_by']='default'
    data['include']='include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,' \
                    'collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,' \
                    'voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,' \
                    'relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;' \
                    'data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics'
    data['limit']=20
    data['offset']=3+20*i

    data=urllib.parse.urlencode(data).encode('utf-8')
    req=urllib.request.Request(url,data,head,method='GET')
    #需指定方法，默认是为POST的
    req = urllib.request.urlopen(req)
    re_data = req.read().decode('gbk')
    print(re_data)