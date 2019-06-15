# 创建了新的tags标签文件后必须重启服务器
from django.utils.safestring import mark_safe
#因为要应用到前端模板语言，必须导入template
from django import template

 #register模块级变量,是所有注册标签和过滤器的数据结构
register = template.Library()

#两种：1.register.filter 2.register.simple_tag
from django.core.cache import cache

@register.simple_tag
def get_online_count():
	online_ips = cache.get("online_ips", [])
	if online_ips:
		online_ips = cache.get_many(online_ips).keys()
		return len(online_ips)
	return 0


