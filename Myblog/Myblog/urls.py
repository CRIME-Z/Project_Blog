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
from django.contrib import admin
from django.urls import path
from django.conf.urls import re_path,include
#静态目录文件设置
from django.conf import settings
from django.conf.urls.static import static

#点地图生成功能
from django.contrib.sitemaps.views import sitemap
from Storm.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap

# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap
}

from Storm.feeds import AllArticleRssFeed
urlpatterns = [
    # 后台管理应用，django自带
    path('admin/', admin.site.urls),
    # 后台编辑器
    re_path(r'mdeditor/', include('mdeditor.urls')),
    # storm博客应用
    re_path(r'^',include('Storm.urls', namespace='blog')), 
    #django-allauth插件
    re_path(r'^accounts/', include('allauth.urls')),
    #django-allauth用户信息扩展
    re_path(r'^accounts/', include('Myaccount.urls',namespace='accounts')),
    # 评论
    re_path(r'^comment/', include('Comment.urls', namespace='Comment')),
    # 网站地图
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #Rss订阅
    re_path(r'^all/rss/$', AllArticleRssFeed(), name='rss'),
    #RESTful Api
    re_path(r'^api/', include('RESTfulApi.urls', namespace='api'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件




