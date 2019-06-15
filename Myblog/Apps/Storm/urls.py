"""Myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import re_path
from Storm import views

app_name='Storm'

urlpatterns = [
    #站点
    path('', views.eosones),
    #主页
    path('homepage/', views.HomepageView.as_view(), name='homepage'), #as_view 方法将一个类转换成一个函数
    #赞助
    path('category/sponsor/', views.SponsorView, name='sponsor'),
    #合作
    path('category/project/', views.ProjectView, name='project'),
    #一级二级菜单分类文章列表
    re_path(r'category/(?P<bigslug>.*?)/(?P<slug>.*?)/',views.CtegoryView.as_view(),name='category'),#django 2.x中用re_path兼容1.x中的url中的方法（如正则表达式）# ?分隔实际的URL和参数,?p数据库里面唯一索引 & URL中指定的参数间的分隔符
    re_path(r'category/(?P<bigslug>.*?)/',views.CtegoryView.as_view(),name='category'),
    # 标签搜索文章列表
    re_path(r'tags/(?P<tagslug>.*?)/', views.CtegoryView.as_view(),name='tag'),
    # 文章详情页面(匹配0个或者任意个不是\n的任意字符)
    re_path(r'^article/(?P<slug>.*?)/$', views.ArticleDetailView.as_view(),name='article'), 
    # 标签搜索ajax请求
    path('ajax/tag/', views.TagAjax),

]
