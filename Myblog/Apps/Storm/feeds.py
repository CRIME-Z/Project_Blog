from django.contrib.syndication.views import Feed

from .models import Article

class AllArticleRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "EOSONES"

    # 通过聚合阅读器跳转到网站的地址
    link = "/all/rss/"

    # 显示在聚合阅读器上的描述信息
    description = "EOSONES的个人博客"

    # 需要显示的内容条目
    def items(self):
        return Article.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body