#自定义模板标签显示文章总数
from django import template
from django.db.models import Count

register = template.Library()
from article.models import ArticlePost

@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n =5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}

@register.simple_tag
def most_commented_articles(n=3):
    #annotate聚合函数，按什么分组相当于group by
    return ArticlePost.objects.annotate(total_comments = Count('comments')).order_by("-total_comments")[:n]