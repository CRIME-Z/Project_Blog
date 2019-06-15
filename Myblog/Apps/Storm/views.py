# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from Storm import models

#站点视图函数
def eosones(request):
	return render(request, 'eosones.html')

#合作视图函数
def ProjectView(request):
	return render(request, 'project.html')

#赞助视图函数
def SponsorView(request):
	return render(request, 'sponsor.html')

#从数据库中获取某个模型列表数据基类ListView#从数据库获取模型的一条记录数据DetailView
from django.views.generic import ListView,DetailView
#主页视图类
class HomepageView(ListView):
	model = models.Article #告诉 Django 我要获取的模型是Article
	template_name = 'homepage.html'  #指定这个视图渲染的模板
	context_object_name = 'articleList'  #指定获取的模型列表数据保存的变量名。这个变量会被传递给模板


from django.core.paginator import Paginator
#分类查找文章列表视图类
class CtegoryView(ListView):
	model=models.Article
	template_name = 'articleList.html' 
	context_object_name = 'articleList' 
	paginate_by = 8 #指定 paginate_by 属性来开启分页功能
	#覆写了父类的 get_queryset 方法获取定制数据
	#类视图中,从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，非命名组参数值保存在实例的 args 属性（是一个列表）里
	def get_queryset(self):
		#get_queryset方法获得全部文章列表
		queryset = super(CtegoryView, self).get_queryset()

		# 导航菜单
		big_slug = self.kwargs.get('bigslug', '')

		# 二级菜单
		slug = self.kwargs.get('slug', '')

		# 标签
		tag_slug = self.kwargs.get('tagslug', '')

		if big_slug:
			big = get_object_or_404(models.BigCategory, slug=big_slug)
			queryset = queryset.filter(category__bigcategory=big)
			if slug:
				if slug=='newest':
					queryset = queryset.filter(category__bigcategory=big).order_by('-create_date')
				elif slug=='hottest':
					queryset = queryset.filter(category__bigcategory=big).order_by('-loves')
				else :
					slu = get_object_or_404(models.Category, slug=slug)
					queryset = queryset.filter(category=slu)
		if tag_slug:
			tlu = get_object_or_404(models.Tag, slug=tag_slug)
			queryset = queryset.filter(tags=tlu)
		return queryset


	#在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的
	def get_context_data(self, **kwargs):
		# 首先获得父类生成的传递给模板的字典。
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		# 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		# 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
		context.update(pagination_data)
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:# 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
			return {}
		# 当前页左边连续的页码号，初始值为空
		left = []
		# 当前页右边连续的页码号，初始值为空
		right = []
		# 标示第 1 页页码后是否需要显示省略号
		left_has_more = False
		# 标示最后一页页码前是否需要显示省略号
		right_has_more = False
		# 标示是否需要显示第 1 页的页码号。
		first = False
		# 标示是否需要显示最后一页的页码号
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number
		# 获得分页后的总页数
		total_pages = paginator.num_pages
		# 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range
		#请求的是第一页的数据
		if page_number == 1:
			#获取了当前页码后连续两个页码
			right = page_range[page_number:(page_number + 2) if (page_number + 2) < paginator.num_pages else paginator.num_pages]
			# 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
			if right[-1] < total_pages - 1:
				right_has_more = True
			# 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
			if right[-1] < total_pages:
				last = True

		# 如果用户请求的是最后一页的数据，
		elif page_number == total_pages:
			#获取了当前页码前连续两个页码
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
			if left[0] > 2:
				left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
			if left[0] > 1:
				first = True

		else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:(page_number + 2) if (page_number + 2) < paginator.num_pages else paginator.num_pages]

            # 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第 1 页和第 1 页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}
		return data



import markdown   #导入markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

import time
#文章详情页类处理
class ArticleDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
	model=models.Article
	template_name = 'article.html' 
	context_object_name = 'article' 
	# url必须pk或者slug或者自定义url和字段
	def get(self, request, *args, **kwargs):
		# 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
		# get 方法返回的是一个 HttpResponse 实例
		# 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
		# 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
		response = super(ArticleDetailView, self).get(request, *args, **kwargs)

        # 注意 self.object 的值就是被访问的文章 article
         # 设置浏览量增加时间判断,同一篇文章两次浏览超过十分钟才重新统计阅览量,作者浏览忽略
		u = self.request.user
		ses = self.request.session
		the_key = 'is_read_{}'.format(self.object.id)   #session中设置已读id字典键
		is_read_time = ses.get(the_key)
		if u != self.object.author:
			if not is_read_time:  
				self.object.update_views()
				ses[the_key] = time.time()  #session中设置当前时间的时间戳
			else:
				now_time = time.time()
				t = now_time - is_read_time
				if t > 60 * 10:
					self.object.update_views()
					ses[the_key] = time.time()

        # 视图必须返回一个 HttpResponse 对象
		return response

	def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染，用model的方法
		article = super(ArticleDetailView, self).get_object(queryset=None)
		md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
		#md实例的convert方法转markdown为html
		article.body = md.convert(article.body)
		#实例 md 就会多出一个 toc 属性
		article.toc = md.toc
		return article
"""
# 覆写 get_context_data 的目的是因为除了将 article 传递给模板外（DetailView 已经帮我们完成），还要把评论表单、post 下的评论列表传递给模板。
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
"""

#标签搜索
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  #取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
def TagAjax(request):
	#if request.is_ajax(): #判断请求头中是否含有X-Requested-With的值
	STKeyword=request.POST['STKeyword']
	STKeywordQS=models.Tag.objects.filter(name__icontains=STKeyword)

	STKeywordDict={}
	n=0
	for x in STKeywordQS:
		STKeywordDict[x.id]=x.name
	return HttpResponse(json.dumps(STKeywordDict))

