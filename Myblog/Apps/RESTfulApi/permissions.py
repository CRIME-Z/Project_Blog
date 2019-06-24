from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
	#只允许作者修改但允许所有人读的权限设置
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
	    # 写入权限需要作者本人
		return request.user and request.user.is_staff