from django.utils.deprecation import MiddlewareMixin#中间件基类
from django.core.cache import cache

class CountMiddleware(MiddlewareMixin):
	#中间件类必须接受一个response参数，就是说必须在中间件类中定义一个__init__函数和一个__call__函数
	#def __init__(self, get_response):
		#self.get_response = get_response

	#def __call__(self, request):
		#return self.get_response(request)

	def process_request(self, request):#在处理url请求之前执行
		#self.online_ips = get_online_count()
		#获取用户IP并设置到cache
		if 'HTTP_X_FORWARDED_FOR' in request.META:
			ip = request.META['HTTP_X_FORWARDED_FOR']
		else:
			ip = request.META['REMOTE_ADDR']
		
		#ip作为key,时间重置，定时5分
		cache.set(ip, 0, 5 * 60)
		#online_ips用来存放所有没有失效的ip的元组
		online_ips = cache.get("online_ips", [])

		if online_ips:
			#根据ip List获取所有没有失效的ip Key，即IP值（更新online_ips）
			online_ips = cache.get_many(online_ips).keys()
			#此时online_ips为dict.keys()类型，需要转为元组
			online_ips=list(online_ips)
		#添加新IP在表中
		if ip not in online_ips:
			online_ips.append(ip)
		#online_ips做为key，用来存放所有的ip[]
		cache.set("online_ips", online_ips)