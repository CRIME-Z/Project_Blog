from django.db import models
from django.conf import settings   #引入定义字段中SEO设置与自定义User
from django.shortcuts import reverse   #查找URL

import re


# 网站导航菜单栏分类表
class BigCategory(models.Model):
	# 导航名称
	name = models.CharField('导航大分类', max_length=20)
	# 用作文章的访问路径，每篇文章有独一无二的标识
	slug = models.SlugField(unique=True)  #此字符串字段可以建立唯一索引
	# 分类页描述
	description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,help_text='用来作为SEO中description,长度参考SEO标准')
	# 分类页Keywords
	keywords = models.TextField('关键字', max_length=240, default=settings.SITE_KEYWORDS,help_text='用来作为SEO中keywords,长度参考SEO标准')
	
	class Meta:  #元信息
		# admin中显示的表名称
		verbose_name = '一级导航'
		verbose_name_plural = verbose_name  #复数形式相同

	def __str__(self):
		return self.name

# 导航菜单分类下的下拉菜单分类
class Category(models.Model):
	# 分类名字
	name = models.CharField('文章分类', max_length=20)
	# 用作分类路径，独一无二
	slug = models.SlugField(unique=True)
	# 分类栏目页描述
	description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,help_text='用来作为SEO中description,长度参考SEO标准')
	# 导航菜单一对多二级菜单,django2.0后定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题
	bigcategory = models.ForeignKey(BigCategory,related_name="Category", on_delete=models.CASCADE,verbose_name='大分类')

	class Meta:#元信息
		# admin中显示的表名称
		verbose_name = '二级导航'
		verbose_name_plural = verbose_name
		 # 默认排序
		ordering = ['name']

	def __str__(self):
		return self.name

	#返回当前的url（一级分类+二级分类）
	def get_absolute_url(self):
		return reverse('blog:category', kwargs={'slug': self.slug, 'bigslug': self.bigcategory.slug})  #寻找路由为blog:category的url
	#返回当前二级分类下所有发表的文章列表
	def get_article_list(self):
		return Article.objects.filter(category=self)

# 文章标签
class Tag(models.Model):
	name = models.CharField('文章标签', max_length=20)
	slug = models.SlugField(unique=True)
	description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,help_text='用来作为SEO中description,长度参考SEO标准')

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name
		ordering = ['id']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('blog:tag', kwargs={'tag': self.name})
	def get_article_list(self):
		#返回当前标签下所有发表的文章列表
		return Article.objects.filter(tags=self)

# 文章关键词，用来作为 SEO 中 keywords
class Keyword(models.Model):
	name = models.CharField('文章关键词', max_length=20)

	class Meta:
		verbose_name = '关键词'
		verbose_name_plural = verbose_name
		ordering = ['name']

	def __str__(self):
		return self.name

from mdeditor.fields import MDTextField  #admin markdown编辑器
import markdown   #导入markdown
# 文章
class Article(models.Model):
	# 文章默认缩略图
	IMG_LINK = '/static/images/article/default.jpg'
	# 文章信息(作者一对多注册用户，这样用户也可以有发文权限)
	#Django2.0表与表之间关联,必须要写on_delete参数(models.CASCADE:删除关联数据,与之关联也删除)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='作者')
	title = models.CharField(max_length=150, verbose_name='文章标题')
	summary = models.TextField('文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
	# 文章内容
	body = MDTextField(verbose_name='文章内容')
	#图片链接
	img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
	#自动添加创建时间
	create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	#自动添加修改时间
	update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
	#浏览点赞整数字段
	views = models.IntegerField('阅览量', default=0)
	loves = models.IntegerField('喜爱量', default=0)
	# 文章唯一标识符
	slug = models.SlugField(unique=True)
	#分类一对多文章  #related_name反向查询
	category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='文章分类')
	#标签多对多文章
	tags = models.ManyToManyField(Tag, verbose_name='标签')
	#文章关键词多对多文章
	keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

	class Meta:
		verbose_name = '博文'
		verbose_name_plural = verbose_name
		ordering = ['-create_date']

	def __str__(self):
		return self.title[:20]
	#返回当前文章的url
	def get_absolute_url(self):
		return reverse('blog:article', kwargs={'slug': self.slug})
	#将内容markdown
	def body_to_markdown(self):
		return markdown.markdown(self.body, extensions=[
			# 包含 缩写、表格等常用扩展
			'markdown.extensions.extra',
			# 语法高亮扩展
			'markdown.extensions.codehilite',
			# 自动生成目录扩展
			'markdown.extensions.toc',
		])

	#点赞+1方法
	def update_loves(self):
		self.loves += 1
		self.save(update_fields=['loves'])  #更新字段

	#浏览+1方法
	def update_views(self):
		self.views += 1
		self.save(update_fields=['views'])  #更新字段

	#前篇方法：当前小于文章并倒序排列的第一个
	def get_pre(self):
		return Article.objects.filter(id__lt=self.id).order_by('-id').first()
	#后篇方法：当前大于文章并正序排列的第一个
	def get_next(self):
		return Article.objects.filter(id__gt=self.id).order_by('id').first()

# 公告
class Activate(models.Model):
	text = models.TextField('公告', null=True)
	#布尔类型
	is_active = models.BooleanField('是否开启', default=False)
	add_date = models.DateTimeField('提交日期', auto_now_add=True)

	class Meta:
		verbose_name = '公告'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.id

# 幻灯片
class Carousel(models.Model):
	number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
	title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='admin与数据库中标题可以为空')
	content = models.CharField('描述', max_length=80)
	img_url = models.CharField('图片地址', max_length=200)
	url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

	class Meta:
		verbose_name = '图片轮播'
		verbose_name_plural = verbose_name
		# 编号越小越靠前，添加的时间约晚约靠前
		ordering = ['number', '-id']

	def __str__(self):
		return self.content[:25]

# 友情链接表
class FriendLink(models.Model):
	name = models.CharField('网站名称', max_length=50)
	description = models.CharField('网站描述', max_length=100, blank=True)
	link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
	logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
	create_date = models.DateTimeField('创建时间', auto_now_add=True)
	is_active = models.BooleanField('是否有效', default=True)
	is_show = models.BooleanField('是否首页展示', default=False)

	class Meta:
		verbose_name = '友情链接'
		verbose_name_plural = verbose_name
		ordering = ['create_date']

	def __str__(self):
		return self.name

	def get_home_url(self):
		"""提取友链的主页"""
		u = re.findall(r'(http|https://.*?)/.*?', self.link)
		home_url = u[0] if u else self.link
		return home_url
	#是否有效方法
	def active_to_false(self):
		self.is_active=False
		self.save(update_fields=['is_active'])
	#是否显示方法
	def show_to_false(self):
		self.is_show = True
		self.save(update_fields=['is_show'])
