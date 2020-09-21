'''
博客应用的url路由
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home),
    path('post/<int:article_id>/', views.article, name="article"),
    path('post/<int:article_id>/get_new_comment/',
         views.get_new_comment, name="get_new_comment"),
    path('post/<int:article_id>/new_comment/',
         views.new_comment, name="new_comment")
]
