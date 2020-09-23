'''
博客视图应用
'''
from datetime import datetime
import json
import markdown
from bs4 import BeautifulSoup
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from blog.models import Article, Category, Comments
from blog.form import CaptchaForm

# Create your views here.


def blog_home(request):
    '''
    博客首页
    '''
    t_catid = request.GET.get(
        "catid")
    catid = 0 if t_catid is None or t_catid == '0' else int(
        request.GET.get("catid"))
    catname = "最新文章" if t_catid is None or t_catid == '0' else Category.objects.get(
        id=catid).name
    page = 1 if request.GET.get(
        "page") is None else int(request.GET.get("page"))
    mobile = is_mobile(request)
    article_list = get_article(page, catid, mobile)
    page_list = get_page(catid, page)
    context = {
        "page": 1,
        "catid": 0,
        "catname": catname,
        "article_list": article_list,
        "page_list": page_list,
        "cats": get_cats()
    }
    if mobile is False:
        return render(request, "blog/article_list.html", context)
    return render(request, "mblog/m_article_list.html", context)


def article(request, article_id):
    '''
    展示文章
    '''
    post = get_object_or_404(Article, id=article_id)
    if post is not None:
        context = {
            "status": True,
            "id": post.id,
            "author": post.author.username,
            "title": post.title,
            "body": markdown.markdown(post.body, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.tables',
            ]),
            "time": post.createTime.strftime('%Y年%m月%d日'),
            "category": post.category.name,
            "cover": post.cover.url,
            "comments": get_comments(post.id, 1),
            "cats": get_cats(),
            "capform": CaptchaForm,
        }
    else:
        context = {"status": False}
    mobile = is_mobile(request)
    if mobile is False:
        return render(request, "blog/post.html", context)
    return render(request, "mblog/m_post.html", context)


def is_mobile(request):
    '''
    判断是否为移动设备默认为非移动设备
    '''
    mobile = False
    devices = ["iPad", "iPhone", "Android"]
    user_agent = request.META.get('HTTP_USER_AGENT')
    for i in devices:
        if i in user_agent:
            mobile = True
            break
    return mobile


def get_article(page, catid, mobile):
    '''
    文章列表获取方法
    '''
    context = []
    words = 80 if mobile is True else 100  # 设置文章列表简介字数
    if catid == 0:
        article_list = Article.objects.all()[(page-1)*4:page*4]
    else:
        article_list = Article.objects.filter(category__id=catid)[
            (page-1)*4:page*4]
    for i in article_list:
        temp = {}
        temp['id'] = i.id
        temp['title'] = i.title
        body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
        ])
        temp['cover'] = i.cover if i.cover is not None else BeautifulSoup(
            body, "lxml").find('img')['src']
        temp['body'] = BeautifulSoup(
            body, "lxml").get_text().strip()[0:words]+"......"
        temp['time'] = i.createTime.strftime('%Y-%m-%d')
        temp['category'] = i.category.name
        context.append(temp)
    return context


def get_page(catid, active_page):
    '''
    获取总共页数
    '''
    if catid == 0:
        page_count = int(Article.objects.count()/4.1)+1
    else:
        page_count = int(Article.objects.filter(
            category__id=catid).count()/4.1)+1
    pages = {}
    pages["data"] = []
    num_active_page = int(active_page)
    if page_count <= 5:
        for i in range(page_count):
            pages["data"].insert(i, i+1)
    else:
        if num_active_page >= page_count-4:
            for i in range(5):
                pages["data"].insert(
                    i, page_count-4+i)
        elif 2 < num_active_page < page_count-4:
            for i in range(5):
                pages["data"].insert(
                    i, num_active_page-2+i)
        else:
            for i in range(5):
                pages["data"].insert(
                    i, i+1)
    pages["total"] = page_count
    pages["active"] = num_active_page
    return pages


def get_cats():
    '''
    获取侧边栏分类列表的方法
    '''
    cat_list = []
    for i in Category.objects.all():
        cat_list.append(
            {"id": i.id, "name": i.name, "count": Article.objects.filter(category=i).count()})
    return cat_list


def get_comments(article_id, active_page):
    '''
    获得评论
    '''
    comments = Comments.objects.filter(article__id=article_id)[
        (active_page-1)*5:active_page*5]
    count = Comments.objects.count()  # 评论数
    json_data = serialize('json', comments)
    comments = json.loads(json_data)
    # 更正序列化后时间变为字符串的错误，恢复为datetime类型

    def changedate(time):
        time['fields']['createTime'] = datetime.strptime(
            time['fields']['createTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime( \
                "%Y年%m月%d日%H:%M:%S")
        return time
    comments = list(map(changedate, comments))
    page_count = int(count/5.1)+1  # 评论页数
    pages = []  # 传递到前端的页码列表
    active_page = int(active_page)
    if page_count <= 5:
        for i in range(page_count):
            pages.insert(i, i+1)
    else:
        if active_page >= page_count-4:
            for i in range(5):
                pages.insert(
                    i, page_count-4+i)
        elif 2 < active_page < page_count-4:
            for i in range(5):
                pages.insert(
                    i, active_page-2+i)
        else:
            for i in range(5):
                pages.insert(
                    i, i+1)
    return {
        "comments": comments,
        "active_page": active_page,
        "total": page_count,
        "page_list": pages
    }


def get_new_comment(request, article_id):
    '''
    获取指定文章指定页码评论
    '''
    page = int(request.GET.get('page'))
    com_json = get_comments(article_id, page)
    return JsonResponse(com_json)


def new_comment(request, article_id):
    '''
    给指定文章添加评论
    '''
    comment = {}
    data = request.POST
    form = CaptchaForm(data)
    if form.is_valid():
        comment['status'] = 1  # 返回状态为1，则验证🐎验证通过
        Comments.objects.create(author=data.get('username'), email=data.get(
            'email'), body=data.get('body'), article=Article.objects.get(id=article_id))
    else:
        comment['status'] = 0  # 返回状态为0，则验证🐎验证不通过
    return JsonResponse(comment)
