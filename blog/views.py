'''
博客视图应用
'''
from bs4 import BeautifulSoup
from django.shortcuts import render
from blog.models import Article
# Create your views here.


def blog_home(request):
    '''
    博客首页
    '''
    mobile = False  # 判断是否为移动设备
    devices = ["iPad", "iPhone", "Android"]
    user_agent = request.META.get('HTTP_USER_AGENT')
    for i in devices:
        if i in user_agent:
            mobile = True
            break
    article_list = get_article(1, 0)
    context = {
        "page": 1,
        "catid": 0,
        "article_list": article_list
    }
    if mobile is False:
        return render(request, "blog/article_list.html", context)
    return render(request, "mblog/m_article_list.html", context)


def get_article(page, catid):
    '''
    文章获取方法
    '''
    context = []
    if catid == 0:
        article_list = Article.objects.all()[(page-1)*4:page*4]
    else:
        article_list = Article.objects.filter(category__id=catid)[
            (page-1)*4:page*4]
    for i in article_list:
        temp = {}
        temp['id'] = i.id
        temp['title'] = i.title
        temp['cover'] = i.cover if i.cover is not None else BeautifulSoup(
            i.body, "lxml").find('img')['src']
        temp['body'] = BeautifulSoup(
            i.body, "lxml").get_text().strip()[0:100]+"......"
        temp['time'] = i.createTime.strftime('%Y-%m-%d')
        temp['category'] = i.category.name
        context.append(temp)
    return context
