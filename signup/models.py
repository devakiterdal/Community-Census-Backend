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
    email = models.EmailField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30,blank=True)
    mother_name = models.CharField(max_length=30,blank=True)
    birthdate = models.DateField(blank=True,null=True,default=None)
    gender = models.CharField(max_length=5,choices=Gender,default="none")
    city = models.CharField(max_length=15,blank=True)
    state = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=15,blank=True)
    pincode = models.IntegerField(blank=True,null=True,default=None)
    phoneno = models.IntegerField(blank=True,null=True,default=None)
    image = models.ImageField(blank=True, upload_to="profileImage")

#content_feed
class posts(models.Model):
    image = models.ImageField(blank=True, upload_to="userimage")
    username = models.ForeignKey(account,on_delete=models.CASCADE,blank=True,default=None,to_field='username')
    description = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True,null=False)
    isActive = models.BooleanField(default=True)
    post_id = models.UUIDField(null=True)


