from django.contrib import admin

# Register your models here.
from Comment import models

#文章
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'belong', 'create_date','loves','content','parent','rep_to')

#写在ArticleAdmin类后面等同于在前面加@
admin.site.register(models.Comment,CommentAdmin)