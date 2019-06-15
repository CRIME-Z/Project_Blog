from django.contrib import admin

# Register your models here.
from Storm import models

# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'

#文章
class ArticleAdmin(admin.ModelAdmin):

	#编辑时除去不可编辑的字段
	exclude = ('views','loves',)
	#编辑时给多选字段增加一个左右添加的框
	filter_horizontal = ('tags', 'keywords')  

	#在查看修改时：给出一个筛选机制，一般按照时间比较好
	date_hierarchy = 'create_date'
	# 在查看修改时：显示的属性，默认第一个字段带有<a>标签
	list_display = ('id', 'title', 'author', 'create_date', 'update_date')
	# 在查看修改时：设置需要添加<a>标签的字段
	list_display_links = ('title',)
	# 在查看修改时：激活过滤器
	list_filter = ('create_date', 'category')
	# 在查看修改时：激活搜索框
	#search_fields = ('tags', 'category')
	# 在查看修改时：制每页显示的对象数量，默认是100
	list_per_page = 50  

	# 限制用户权限，只能看到自己编辑的文章
	def get_queryset(self, request):
		qs = super(ArticleAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(author=request.user)
#写在ArticleAdmin类后面等同于在前面加@
admin.site.register(models.Article,ArticleAdmin)  

#文章标签
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'slug')

#二级导航
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'slug')

#一级导航
@admin.register(models.BigCategory)
class BigCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'slug')

# 幻灯片
@admin.register(models.Carousel)
class CarouselAdmin(admin.ModelAdmin):
	list_display = ('number', 'title', 'content', 'img_url', 'url')

# 文章关键词
@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
	list_display = ('name', 'id')

# 友情链接表
@admin.register(models.FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
	#在查看修改的时候显示的属性，默认第一个字段带有<a>标签
	list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
	# 设置需要添加<a>标签的字段
	date_hierarchy = 'create_date'
	# 激活过滤器
	list_filter = ('is_active', 'is_show')