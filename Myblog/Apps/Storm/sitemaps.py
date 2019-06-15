# -*- coding: utf-8 -*-
#网站地图
from django.contrib.sitemaps import Sitemap
from Storm.models import Article, Category, Tag
#统计分类下的文章数量的功能
from django.db.models.aggregates import Count

#问题：为什么要配置storm.url的name才能显示？？？

# 文章聚类
class ArticleSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 1.0

	def items(self):
		return Article.objects.all()

	def lastmod(self, obj):
		return obj.update_date


# 分类聚类
class CategorySitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.8

	def items(self):
		return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

	def lastmod(self, obj):
		return obj.article_set.first().create_date


# 标签聚类
class TagSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.8

	def items(self):
		return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

	def lastmod(self, obj):
		return obj.article_set.first().create_date
		
#问题：tag反向解析一直出错，只有自定义location
	def location(self, obj):
		return '/tags/%s' % obj.slug