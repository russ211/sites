from django.contrib import admin

# Register your models here.
from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user" , "birth" , "phone" , "address" , "school" , "profession" , "company" , "aboutme" , "photo")
    list_filter = ("user" , "phone")



admin.site.register(UserInfo , UserInfoAdmin)