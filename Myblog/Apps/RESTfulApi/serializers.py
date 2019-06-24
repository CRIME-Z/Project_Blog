
from rest_framework import serializers
from Myaccount.models import User
from Storm.models import Article, Tag, Category,FriendLink
from Comment.models import Comment,UserLike

#用户信息
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'link', 'avatar','email') #插件allauth中关联User模型定义的email字段

#标签
class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

#分类
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__' #指定字段

#文章
class ArticleSerializer(serializers.ModelSerializer):
	#自定义字段覆盖默认字段
	author = serializers.ReadOnlyField(source='author.username') #自定义作者名字字段
	keywords = serializers.SlugRelatedField(  #自定义关键字字段(只关联name)
		many=True, #一对多
		read_only=True, #只读字段
		slug_field='name'
    )
	category = CategorySerializer(read_only=True) #嵌套序列
	tags = TagSerializer( #嵌套序列
		many=True, #一对多
		read_only=True, #只读字段
    )

	class Meta:
		model = Article
		exclude = ('body',)#除去指定的某些字段

#评论
class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__' #指定字段

#用户点赞文章
class UserLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLike
		fields = '__all__' #指定字段
#友情链接
class FriendLinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendLink
		fields = ('name','link')#指定字段