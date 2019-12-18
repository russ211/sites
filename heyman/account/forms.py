from django import forms
from django.contrib.auth.models import User

from .models import UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)#为字段使用不同的窗口小部件，则只需widget在字段定义上使用该参数即可


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password" , widget= forms.PasswordInput)
    password2 = forms.CharField(label="ConfirmPassword" , widget= forms.PasswordInput)

    #class Meta做为嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准。
    class Meta:
        model = User
        fields = ("username" , "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次输入的密码不匹配")
        return cd['password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("birth" , "phone" , "school" , "company" , "profession" , "address" , "aboutme")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )
