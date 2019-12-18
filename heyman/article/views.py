from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm
from .models import ArticleColumn, ArticlePost, ArticleTag


@login_required(login_url = 'account/login/')
@csrf_exempt #另一种操作POST时的加密机制
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user = request.user)
        column_form = ArticleColumnForm()
        context = {
            "columns" : columns,
            "column_form" : column_form
        }
        return render(request , "article/article_column.html" , context)
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user = request.user , column = column_name)
        if columns:
            return HttpResponse("已存在此记录")
        else:
            ArticleColumn.objects.create(user = request.user , column = column_name )
            return HttpResponse("1")

@login_required(login_url = 'account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id = column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url = 'account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id = column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url = 'account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id = request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag = atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        context = {
            "article_post_form" : article_post_form ,
            "article_columns" : article_columns,
            "article_tags" : article_tags
        }
        return render(request , "article/column/article_post.html" , context)

@login_required(login_url = 'account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author = request.user)
    paginator = Paginator(articles_list , 8)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    context = {
        "articles" : articles ,
        "page" : current_page
    }
    return render(request , "article/column/article_list.html" , context)

@login_required(login_url = 'account/login/')
def article_detail(request , id , slug):
    article = get_object_or_404(ArticlePost , id = id , slug = slug)
    context = {
        "article" : article
    }
    return render(request , "article/column/article_detail.html" , context)

@login_required(login_url = 'account/login/')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id = article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url = 'account/login/')
@csrf_exempt

def redit_article(request , article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id = article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        print(this_article_column)
        context = {
            "article" : article , "article_columns" : article_columns , "this_article_column" : this_article_column , "this_article_form":this_article_form
        }
        return render(request , "article/column/redit_article.html" , context)
    else:
        redit_article = ArticlePost.objects.get(id = article_id)
        try:
            redit_article.column = request.user.article_column.get(id = request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")

@login_required(login_url = 'account/login/')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author = request.user)
        article_tag_form = ArticleTagForm()
        context = {
            "article_tags" : article_tags,
            "article_tag_form" : article_tag_form
        }
        return render(request , "article/tag/tag_list.html" , context)

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data= request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry , the form is not valid.")

@login_required(login_url = 'account/login/')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id = tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

