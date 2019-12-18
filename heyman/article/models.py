from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from slugify import slugify


class ArticleColumn(models.Model):
    user = models.ForeignKey(User , related_name='article_column' , on_delete= models.CASCADE)
    column = models.CharField(max_length= 200)
    created = models.DateField(auto_now_add=True)#auto_now_add 创建或添加对象时的时间, 修改或更新对象时, 不会更改时间

    def __str__(self):
        return self.column

class ArticleTag(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="tag")
    tag = models.CharField(max_length=500)


    def __str__(self):
        return self.tag

class ArticlePost(models.Model):
    author = models.ForeignKey(User , on_delete= models.CASCADE , related_name="article")#related_name 在定义主表的外键的时候，给这个外键定义好一个名称
    title = models.CharField(max_length= 200)
    slug = models.SlugField(max_length= 200)
    column = models.ForeignKey(ArticleColumn , on_delete= models.CASCADE , related_name= "article_column")
    body = models.TextField()
    created = models.DateTimeField(default= timezone.now)
    updated = models.DateTimeField(auto_now= True)#对对象进行操作(创建/添加/修改/更新),时间都会随之改变
    users_like = models.ManyToManyField(User , related_name="articles_like" , blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name="article_tag", blank=True)

    class Meta:
        #表示文章列表按照发布时间倒序排列
        ordering = ("-updated" ,)
        #对数据库中的这两个字段建立索引，以后就可以通过每篇文章的id和slug来获取该文章对象了，这样建立索引以后，能提高读取文章对象的速度
        index_together = (('id' , 'slug'),)
    def __str__(self):
        return self.title

    #重写save()方法，是为了实现 self.slug = slugify(self.title)，然后再执行父类的save方法
    def save(self , *args , **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args , **kargs)

    #获取某篇文章的URL ，article_detail需先登录
    def get_absolute_url(self):
        return reverse("article:article_detail" , args = [self.id , self.slug])
    #重新定义不需要登录
    def get_url_path(self):
        return reverse("article:article_content" , args=[self.id , self.slug])

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost , on_delete= models.CASCADE , related_name= "comments")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created' ,)
        def __str__(self):
            return "Comment by {0} on {1}".format(self.commentator.username , self.article)

