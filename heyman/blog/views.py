from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import BlogArticles


def blog_list(request):
    blogs = BlogArticles.objects.all()
    context = {
        "blogs" : blogs
    }
    return render(request , "blog/blog_list.html" , context)

def blog_detail(request , article_id):
    article = get_object_or_404(BlogArticles , id = article_id)
    pub = article.publish
    context = {
        "article" : article,
        "publish" : pub
    }
    return render(request , "blog/blog_detail.html" , context)
