from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.


def show_home(request):
    return render(request, 'index.html', {'url':'http://cdn.gxstar123.cn/jiuzhai-unsplash.jpg'})


def get_background():
    '''获得每日bing图片作为首页背景
    输入：无
    返回：dict(图片地址)
    '''
    context = {}
    origin_url = "https://cn.bing.com/HPImageArchive.aspx?idx=0&n=1"
    xml_file = requests.get(origin_url).content
    bs_parse = BeautifulSoup(xml_file, "lxml")
    result_url = "https://cn.bing.com"+bs_parse.url.string
    context['url'] = result_url
    return context
