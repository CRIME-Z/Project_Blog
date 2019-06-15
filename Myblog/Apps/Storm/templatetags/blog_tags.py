# 创建了新的tags标签文件后必须重启服务器
from django.utils.safestring import mark_safe
#因为要应用到前端模板语言，必须导入template
from django import template
from Storm.models import Tag,FriendLink,Article

 #register模块级变量,是所有注册标签和过滤器的数据结构
register = template.Library()
#两种：1.register.filter 2.register.simple_tag

#获取所有标签
@register.simple_tag
def get_tags():
	lis = Tag.objects.all()
	return lis

#获取所有link
@register.simple_tag
def get_friendLinks():
	lis = FriendLink.objects.all()
	return lis

#获取文章所有标签
@register.simple_tag
def get_article_tag(article_id):
	return Tag.objects.filter(article=article_id)

# 获取下一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_next(article_id):
	has_next = False
	id_next = int(article_id)
	article_id_max = Article.objects.all().order_by('-id').first()
	id_max = article_id_max.id
	while not has_next and id_next <= id_max:
		id_next += 1
		article_next = Article.objects.filter(id=id_next).first()
		if not article_next:
			id_next += 1
		else:
			has_next = True
	if has_next:
		article = Article.objects.filter(id=id_next).first()
		return article
	else:
		return

# 获取前一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_previous(article_id):
	has_previous = False
	id_previous = int(article_id)
	while not has_previous and id_previous >= 1:
		id_previous -= 1
		article_previous = Article.objects.filter(id=id_previous).first()
		if not article_previous:
			id_previous -= 1
		else:
			has_previous = True
	if has_previous:
		article = Article.objects.filter(id=id_previous).first()
		return article
	else:
		return