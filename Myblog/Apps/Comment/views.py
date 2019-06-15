from django.shortcuts import render

# Create your views here.

from Storm.models import Article
from Myaccount.models import User
from Comment.models import Comment,UserLike
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import re
import json

#评论
@csrf_exempt
@require_POST
def AddcommentView(request):
	if request.is_ajax():
		data = request.POST
		# 评论内容
		new_content = data.get('arciclecomment')
		# 评论对象文章
		comment_post_ID = data.get('comment_post_ID')
		# 评论者
		author = data.get('comment_author')
		# 评论者网址
		#url = data.get('url', '')
		# 评论对象，父级对象，就是评论的是谁
		comment_parent = data.get('comment_parent')
		# 获取用户信息
		auser = User.objects.get(username=author)
		# 获取文章信息
		the_article = Article.objects.get(id=comment_post_ID)

		if comment_parent == '0':
			new_comment = Comment(author=auser, content=new_content, belong=the_article, parent=None, rep_to=None)
		else:
			comment_repto=data.get('comment_rep')
			repto=Comment.objects.get(id=comment_repto)
			parent = Comment.objects.get(id=comment_parent)
			new_comment = Comment(author=auser, content=new_content, belong=the_article, parent=parent, rep_to=repto)
		new_comment.save()
		
		success={}
		success={"success":"success"}
		return HttpResponse(json.dumps(success))

#点赞
import json
@csrf_exempt
def likeView(request):
	post_ID=request.POST['like_post_ID']
	author_ID=request.POST['like_author']

	post = Article.objects.get(id=post_ID)
	author = User.objects.get(id=author_ID)
	
	UserLike.objects.create(author=author, belong=post)
	post.update_loves()
	love=post.loves
	print(love)
	data={}
	data={"love":love}
	return HttpResponse(json.dumps(data))