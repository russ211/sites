from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BlogArticles(models.Model):
    title = models.CharField(max_length= 300)
    #通过User类反向查询到BlogArticles，这个参数可以不设置，Django默认以模型小写作为反向关联名，以后从User对象反向关联到BlogArticles，可使用user.blog_posts
    author = models.ForeignKey(User , related_name= "blog_posts" , on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default= timezone.now)
