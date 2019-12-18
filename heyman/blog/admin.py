from django.contrib import admin

# Register your models here.
from .models import BlogArticles

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title" , "author" , "publish")
    list_filter = ("publish" , "author")
    search_fields = ("title" , "body")
    # raw_id_fields = ("author",) 显示外键信息
    #按日期月份筛选
    date_hierarchy = "publish"
    ordering = ["publish" , "author"]



admin.site.register(BlogArticles , BlogArticlesAdmin)