'''
博客应用的url路由
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home),
]
