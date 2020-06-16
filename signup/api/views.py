from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics


from signup.models import account
from . serializers import userRegisterSerializer

from rest_framework.response import Response 

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from signup import models
import uuid
#login

# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT

# from login.models import account
from . serializers import UserLoginSerializer

from django.contrib.auth import login as django_login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from signup.models import account
import uuid

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.generics import CreateAPIView


from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

#profile
from signup.models import profile
from . serializers import ProfileAPI


#content_feed
from signup.models import posts
from rest_framework import status, viewsets
from signup.api.serializers import contentfeedSerializer
from datetime import datetime

#POSTDELETEAPIVIEW
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView
@api_view(['POST',])
def register(request):
    if request.method == 'POST':
        serializer = userRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            acc = serializer.save()
            data['response'] = "Successfully registered"
            data['username'] = acc.username
            data['email'] = acc.email
            data['first_name'] = acc.first_name
            data['last_name'] = acc.last_name
            data['unique_id'] = acc.unique_id
        else:
            data = serializer.errors
        return Response(data)        
    
# def registerPage(request):
#     return render(request, 'register.html')
        # return Response({"token":Token.key},status=200)

class createAPIView(CreateAPIView):
    serializer = UserLoginSerializer
    queryset = models.account.objects.all()

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = UserLoginSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            print(request.session.get_expiry_age())
            print(request.session.get_expiry_date())
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def profileView(request):
    if request.method == 'POST':
        serializer = ProfileAPI(data=request.data)
        info = {}
        if serializer.is_valid():
            profileData = serializer.save()
            info['response'] = "Profile created."
            info['first_name'] = profileData.first_name
            info['last_name'] = profileData.last_name
            info['father_name'] = profileData.father_name
            info['mother_name'] = profileData.mother_name
            info['birthdate'] = profileData.birthdate
            info['gender'] = profileData.gender
            info['phoneno'] = profileData.phoneno
            info['email'] = profileData.email
            info['city'] = profileData.city
            info['state'] = profileData.state
            info['country'] = profileData.country
            info['pincode'] = profileData.pincode
        else:
            info =serializer.errors
        return Response(info)   

#content_feed_view
@api_view(['GET','POST',])
def content_feed(request):
    #content_feed_fetching
    if request.method == 'GET':
        fetchcontent = models.posts.objects.all()
        serializer = contentfeedSerializer(fetchcontent, many=True)
        return Response(serializer.data)
        
    #content_feed_inserting
    elif request.method == 'POST':
        serializer = contentfeedSerializer(data=request.data)
        contentinfo = {}
        if serializer.is_valid():
            contentdata = serializer.save()
            contentinfo['response'] = "Content feeded."
            contentinfo['post_id'] = contentdata.post_id
            contentinfo['description'] = contentdata.description
            contentinfo['post_time'] = contentdata.post_time
        else:
            contentinfo = serializer.errors
        return Response(contentinfo)  

@api_view(['GET','POST','DELETE',])
def content_feed_pk(request,post_id):
    try:
        post = posts.objects.get(post_id=post_id)
    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #content_feed_fetching
    if request.method == 'GET':
        fetchcontent = models.posts.objects.all()
        serializer = contentfeedSerializer(fetchcontent, many=True)
        return Response(serializer.data)
        
    #content_feed_inserting
    elif request.method == 'POST':
        serializer = contentfeedSerializer(data=request.data)
        contentinfo = {}
        if serializer.is_valid():
            contentdata = serializer.save()
            contentinfo['response'] = "Content feeded."
            contentinfo['post_id'] = contentdata.post_id
            contentinfo['description'] = contentdata.description
            contentinfo['post_time'] = contentdata.post_time
        else:
            contentinfo = serializer.errors
        return Response(contentinfo)  

    #POST DELETE 
    elif request.method == 'DELETE':
        # serializer = contentfeedSerializer(data=request.data)
        # contentinfo = {}
        # if serializer.is_valid():
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




 
