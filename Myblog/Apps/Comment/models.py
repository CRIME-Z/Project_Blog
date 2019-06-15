from django.db import models

# Create your models here.
from django.conf import settings
from Storm.models import Article
from Myaccount.models import User

import markdown
# 评论信息表
class Comment(models.Model):
	author = models.ForeignKey(User, related_name='%(class)s_related',on_delete=models.CASCADE, verbose_name='评论人')
	belong = models.ForeignKey(Article, related_name='article_comments',on_delete=models.CASCADE, verbose_name='所属文章')
	create_date = models.DateTimeField('创建时间', auto_now_add=True)
	loves = models.IntegerField('喜爱量', default=0)
	content = models.TextField('评论内容')
	parent = models.ForeignKey('self', verbose_name='父评论', related_name='%(class)s_child_comments',on_delete=models.CASCADE, blank=True, null=True)
	rep_to = models.ForeignKey('self', verbose_name='回复', related_name='%(class)s_rep_comments',on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		verbose_name = '文章评论'
		verbose_name_plural = verbose_name
		ordering = ['create_date']


	def __str__(self):
		return self.content[:20]

	def content_to_markdown(self):
		to_md = markdown.markdown(
                                  safe_mode='escape',
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
		return to_md

#用户点赞表
class UserLike(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE,)
	belong = models.ForeignKey(Article,on_delete=models.CASCADE, verbose_name='所属文章')
