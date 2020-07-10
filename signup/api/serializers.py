from rest_framework import serializers
from signup.models import account

from django.contrib.auth.models import User
from django.http import HttpResponse
import uuid
from django.contrib.auth.models import AbstractUser

#login

from rest_framework import serializers
from signup.models import account

from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.response import Response

#profile
from signup.models import profile
from signup.models import posts

class userRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ['username','email','first_name','last_name','password','unique_id']

        extra_kwargs = {
            'password': {'write_only' : True}
        }

    def create(self, validated_data):
        acc = account.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            password = self.validated_data['password']
        )     

        pro = profile.objects.create(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
        ) 
        acc.unique_id = uuid.uuid4() 
        acc.save()
        return acc

class UserLoginSerializer(serializers.ModelSerializer):
    # unique_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(required=False,allow_blank=True)
    last_name = serializers.CharField(required=False,allow_blank=True)
    username = serializers.CharField(required=False,allow_blank=True)
    email = serializers.EmailField(required=False,allow_blank=True)
    class Meta:
        model = account
        fields = [
            'email','password','username','first_name','last_name'
        ]
        extra_kwargs = {
            "password":  {"write_only":True}
        }
    
    def validate(self,data):
        email = data.get("email",None)
        password = data["password"] 

        if not email:
            raise ValidationError("Email is required")

        users = account.objects.filter(
            Q(email = email)  
        ).distinct()

        if users.exists() and users.count() == 1:
            user_obj = users.first()
        else:
            raise ValidationError("Email is not valid")

        if user_obj:
            if not user_obj.password == data["password"]:
                raise ValidationError("password mismatch")
            print("******************************************")         
        data = user_obj
        return data


class ProfileAPI(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ['first_name','last_name','father_name','mother_name','birthdate','gender','phoneno','email','city','state','country','pincode', 'image' ]

#posts_feed
#content_feed_inserting and fetching
class contentfeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = ['description','post_time','post_id','username','image']
    
    def save(self):
        contentdata = posts(
            description = self.validated_data['description'],
            username = self.validated_data['username'],
            image = self.validated_data['image']
        )
        contentdata.post_id = uuid.uuid4() 
        contentdata.save()
        return contentdata

class PostsSerializerWithoutPostId(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = ['description','post_time','post_id','username','image']
