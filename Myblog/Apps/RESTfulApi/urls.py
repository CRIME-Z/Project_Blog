from django.urls import path
from django.conf.urls import re_path,include
from . import views as api_views
from rest_framework.routers import DefaultRouter

app_name='RESTfulApi'

router = DefaultRouter()
router.register(r'users', api_views.UserListSet)
router.register(r'articles', api_views.ArticleListSet)
router.register(r'tags', api_views.TagListSet)
router.register(r'categorys', api_views.CategoryListSet)
router.register(r'friendLink', api_views.FriendLinkListSet)
router.register(r'comment', api_views.CommentListSet)
router.register(r'userlike', api_views.UserLikeListSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]