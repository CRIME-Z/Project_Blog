# 创建了新的tags标签文件后必须重启服务器
from django.utils.safestring import mark_safe
#因为要应用到前端模板语言，必须导入template
from django import template
from Comment.models import Comment,UserLike
from Storm.models import Article
from Myaccount.models import User

 #register模块级变量,是所有注册标签和过滤器的数据结构
register = template.Library()
#两种：1.register.filter 2.register.simple_tag

#获取一个文章的评论总数
@register.simple_tag
def get_comment_count(entry=0):
	lis = Comment.objects.filter(belong_id=entry)
	return lis.count()

#获取一个文章的父评论列表
@register.simple_tag
def get_parent_comments(entry=0):
	lis = Comment.objects.filter(belong_id=entry,parent=None)
	return lis

# 获取一个父评论的子评论列表
@register.simple_tag
def get_child_comments(com):
	lis = Comment.objects.filter(parent=com)
	return lis

# 评论转md方法
import markdown
@register.simple_tag
def content_to_markdown(content):
    to_md = markdown.markdown(
        content,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        #'markdown.extensions.codehilite',
        ])
    return to_md

#查找是否点赞
@register.simple_tag
def is_likes(Post_id,User_id):
    post = Article.objects.get(id=Post_id)
    user = User.objects.get(id=User_id)
    #exists()查询是否包含，返回布尔值!!!
    is_exist=UserLike.objects.all().filter(author=User_id,belong=post).exists()
    return is_exist


"""
# 递归查找父评论
def find_father(dic, comment_obj):
    # 对字典中的每一组元素进行循环操作
    for k, v_dic in dic.items():
        # 如果k等于comment_obj的父节点，那么表示找到了父亲。
        if k == comment_obj.parent:
            # 找到了父亲，认祖归宗，把自己归位到父亲下面，并给将来的儿子留个位置
            dic[k][comment_obj] = {}
            # 找到了父亲，处理完毕，返回
        else:
            # 刚才没找到，剥一层，接着往下找。
            find_father(dic[k], comment_obj)
"""



