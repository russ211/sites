import base64
import os

from PIL import Image
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
# from heyman.heyman import settings
# from heyman.heyman.settings import MEDIA_ROOT
from django.urls import reverse
from wheel.util import StringIO

from .models import UserInfo
from .forms import LoginForm, RegistrationForm, UserForm, UserInfoForm


# def user_login(request):
#     if request.method == "POST":
#         login_form = LoginForm(request.POST)
#         # 传递给表单的数据是否符合表单类属性要求的
#         if login_form.is_valid():
#             #以字典的形式返回实例的具体数据
#             cd = login_form.cleaned_data
#             #验证账号密码是否正确,验证成功返回一个user对象,失败则返回None
#             user = authenticate(username = cd['username'] , password = cd['password'])
#             print(user)
#             print(cd['username'] , cd['password'])
#             if user:
#                 #该函数接受一个 HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（ session ）框架把用户的ID保存在该会话中
#                 login(request , user)
#                 return HttpResponse("Welcome You. You have been authenticated successfully")
#             else:
#                 return HttpResponse("Sorry. Your username or pasword is not right.")
#         else:
#             return HttpResponse("Invalid login")
#
#     if request.method == "GET":
#         login_form = LoginForm()
#         context = {
#             "form" : login_form
#         }
#         return render(request , "account/login.html" , context)

def user_register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)

        #user_form.is_valid() 会触发 forms 中的 clean_password2 函数
        # if user_form.is_valid() * userprofile_form.is_valid():
        print(user_form)
        if user_form.is_valid():
            # user_form.save(commit=False) 仅生成一个数据对象，不会保存到数据库表
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            UserInfo.objects.create(user = new_user)
            return HttpResponseRedirect(reverse("account:user_login")) #reverse()对已命名的URL进行反向解析，还传递相应的参数（args或带key的参数kargs)
        else:
            return HttpResponse("抱歉，您不能注册。")
    else:
        user_form = RegistrationForm()
        context = {
            "form" : user_form
        }
        return render(request , "account/register.html" , context)

@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username = request.user.username)
    userinfo = UserInfo.objects.get(user = user)
    context = {
        "user" : user ,
        "userinfo" : userinfo
    }
    return render(request , "account/myself.html" , context)

@login_required(login_url='/account/login')
def myself_edit(request):
    userinfo = UserInfo.objects.get(user = request.user) if hasattr(request.user,'userinfo') else UserInfo.objects.create(user = request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userinfo.birth = userinfo_cd['birth']
            userinfo.phone = userinfo_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance= request.user)

        userinfo_form = UserInfoForm(initial={"birth":userinfo.birth , "phone":userinfo.phone ,"school":userinfo.school ,"company":userinfo.company , "profession":userinfo.profession , "address":userinfo.address ,"aboutme":userinfo.aboutme})
        # print(userinfo_form["photo"])
        context = {
            "user_form" : user_form,
            "userinfo_form" : userinfo_form,
            "avatar" : userinfo.photo
        }
        print(userinfo.photo)
        return render(request , "account/edit_my_information.html" , context)

@login_required(login_url= '/account/login')
def my_image(request):
    if request.method == 'POST':
        img = request.FILES.get('avatar')
        if img:
            print(img.name)
        else:
            print("no pic!")
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        # print(img , len(img))
        # with open(filepath , 'wb') as fp:
        # filepath = os.path.join(settings.MEDIA_ROOT , img.name)
        #     for part in img.chunks():
        #         fp.write(part)
        # uf = UserInfoForm(request.Files)
        # if uf.is_valid():
        #     avatar = uf.cleaned_data['img']
        # userinfo = UserInfo.objects.create(photo = avatar)
        # userinfo.save()

        return  HttpResponse("上传成功！")
    else:
        return render(request , 'account/imagecrop.html' , )