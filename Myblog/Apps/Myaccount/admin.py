from django.contrib import admin


# Register your models here.
from Myaccount.models import User

#文章标签
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username','link', 'avatar')
