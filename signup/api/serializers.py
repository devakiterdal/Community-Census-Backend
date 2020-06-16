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

    def save(self):
        acc = account(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            password = self.validated_data['password']
        )      
        acc.unique_id = uuid.uuid4() 
        acc.save()
        return acc

class UserLoginSerializer(serializers.ModelSerializer):
    # unique_id = serializers.UUIDField(read_only=True)
    # username = serializers.CharField(required=False,allow_blank=True)
    email = serializers.EmailField(required=False,allow_blank=True)
    class Meta:
        model = account
        fields = [
            'email','password'
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
        return data

class ProfileAPI(serializers.ModelSerializer):
    
    class Meta:
        model = profile
        fields = ['first_name','last_name','father_name','mother_name','birthdate','gender','phoneno','email','city','state','country','pincode']

    def save(self):
        profileData = profile(
	    first_name = self.validated_data['first_name'],
        last_name = self.validated_data['last_name'],
        father_name = self.validated_data['father_name'],
        mother_name = self.validated_data['mother_name'],
        birthdate = self.validated_data['birthdate'],
        gender = self.validated_data['gender'],
	    phoneno = self.validated_data['phoneno'],
	    email = self.validated_data['email'],	
        city = self.validated_data['city'],
        state = self.validated_data['state'],
	    country = self.validated_data['country'],
        pincode = self.validated_data['pincode']
        )
        profileData.save()      
        return profileData 

#posts_feed
#content_feed_inserting and fetching
class contentfeedSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='account.username')
    class Meta:
        model = posts
        fields = ['post_id', 'description','post_time']
    
    def save(self):
        contentdata = posts(
            description = self.validated_data['description']
            # post_created = self.validated_data['post_created']
        )
        contentdata.post_id = uuid.uuid4() 
        contentdata.save()
        return contentdata

