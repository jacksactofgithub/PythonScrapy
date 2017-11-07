__author__ = 'liushuo'
import urllib

tmp = 'data-original=\"https://pic1.zhimg.com/df7507ed69a54b936381257ccdca0f88_r.jpg\"'

tmp = tmp.replace('data-original=','')
tmp = tmp.replace('\"','')
print(tmp)