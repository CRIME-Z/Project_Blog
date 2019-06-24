from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from Myaccount.models import User
from Comment.models import Comment,UserLike
from Storm.models import Article, Tag, Category,FriendLink
from .serializers import UserSerializer, ArticleSerializer, TagSerializer, CategorySerializer,FriendLinkSerializer,CommentSerializer,UserLikeSerializer

# 用 viewsets 构建 View
class UserListSet(viewsets.ModelViewSet):
    # 处理 /api/users/ GET, 处理 /api/users/<pk>/ GET
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class TagListSet(viewsets.ModelViewSet):
    # 处理 /api/tags/ GET POST, 处理 /api/tags/<pk>/ GET
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class FriendLinkListSet(viewsets.ModelViewSet):
    # 处理 /api/friendLink/ GET POST, 处理 /api/friendLinks/<pk>/ GET
    queryset = FriendLink.objects.all()
    serializer_class = TagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class CategoryListSet(viewsets.ModelViewSet):
    # 处理 /api/categorys/ GET POST, 处理 /api/categorys/<pk>/ GET
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class ArticleListSet(viewsets.ModelViewSet):
    # 处理 /api/articles/ GET POST , 处理 /api/articles/<pk>/ GET PUT PATCH DELETE
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    # 重写 perform_create, user 信息不在 request.data 中, 在保存时加入 user 信息
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class CommentListSet(viewsets.ModelViewSet):
    # 处理 /api/comment/ GET POST, 处理 /api/comment/<pk>/ GET
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class UserLikeListSet(viewsets.ModelViewSet):
    # 处理 /api/userlikes/ GET POST, 处理 /api/userlikes/<pk>/ GET
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)








