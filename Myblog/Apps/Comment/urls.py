from django.urls import path
from django.conf.urls import re_path
from Comment import views

app_name='Comment'

urlpatterns = [
        # 评论
        re_path(r'^add/$', views.AddcommentView, name='add_comment'),
        # 点赞
        path('addlike/', views.likeView), 
]
