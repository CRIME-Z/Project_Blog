from django.conf.urls import re_path
from . import views

app_name = "Myaccount"

urlpatterns = [
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
    
]
