from django.shortcuts import render,HttpResponse
from bs4 import BeautifulSoup
import requests

# Create your views here.


def show_home(request):
    return render(request, 'index.html', {'url': 'http://cdn.gxstar123.cn/jiuzhai-unsplash.jpg'})
