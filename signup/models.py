# Create your models here.
from django.db import models
import uuid

class account(models.Model): 
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(max_length=30,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=8)
    unique_id = models.UUIDField(null = True)
    # token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username

class profile(models.Model):
    oneword = (
        ('yes',"Yes"),
        ('no',"No"),
        ('none',"None")
    )
    Gender = (
        ('m',"Male"),
        ('f',"Female"),
        ('other',"other"),
        ('none',"None")
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    birthdate = models.DateField()
    gender = models.CharField(max_length=5,choices=Gender,default="none")
    phoneno = models.IntegerField()
    email = models.EmailField(max_length=20)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    country = models.CharField(max_length=15)
    pincode = models.IntegerField()

#content_feed
class posts(models.Model):
    post_id = models.UUIDField(default=None,primary_key=True)
    # username = models.ForeignKey(account,on_delete=models.CASCADE,blank=True,default=None)
    description = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True,null=False)
    isActive = models.BooleanField(default=False)
    # dateTime = models.DateTimeField(auto_now_add=True)


