from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE , unique= True)
    birth = models.DateField(null= True , blank= True)
    phone = models.CharField(max_length= 20 , blank= True)
    school = models.CharField(max_length= 100 , blank= True)
    company = models.CharField(max_length= 100 , blank= True)
    profession = models.CharField(max_length= 100 , blank= True)
    address = models.CharField(max_length= 100 , blank= True)
    aboutme = models.TextField(blank= True)
    photo = models.ImageField(blank = True , upload_to= "avatars")

    def __str__(self):
        return "user:{}".format(self.user.username)