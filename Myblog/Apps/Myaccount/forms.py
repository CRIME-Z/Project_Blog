#创建两个表单：一个是更新用户资料时使用，一个是重写用户登录表单。

from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
	class Meta:
		# 关联的数据库模型，这里是用户模型
		model = User
		# 验证后可以修改的数据
		fields = ['nickname','link', 'avatar']