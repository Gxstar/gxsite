'''
博客视图应用
'''
from bs4 import BeautifulSoup
from django.shortcuts import render
from blog.models import Article, Category
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
    # 判断是否为移动设备默认为非移动设备
    mobile = False
    devices = ["iPad", "iPhone", "Android"]
    user_agent = request.META.get('HTTP_USER_AGENT')
    for i in devices:
        if i in user_agent:
            mobile = True
            break
    article_list = get_article(page, catid)
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
    post = Article.objects.filter(id=article_id)
    if post[0] is not None:
        context = {
            "status": True,
            "id": post[0].id,
            "author": post[0].author.username,
            "title": post[0].title,
            "body": post[0].body,
            "time": post[0].createTime.strftime('%Y年%m月%d日'),
            "category": post[0].category.name,
            "cover": post[0].cover,
            "cats": get_cats()
        }
    else:
        context = {"status": False}
    return render(request, "blog/post.html", context)


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


def get_page(catid, active_page):
    '''
    获取总共页数
    '''
    if catid == 0:
        page_count = int(Article.objects.count()/4)+1
    else:
        page_count = int(Article.objects.filter(
            category__id=catid).count()/4)+1
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
