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
from signup.api.serializers import PostsSerializerWithoutPostId, contentfeedSerializer
from datetime import datetime

#POSTDELETEAPIVIEW
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView

from django.db.models import Count
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

#user_login
@api_view(['POST',])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            newData = serializer.data
        else:
            data = serializer.errors
        return Response(newData)  

   
@api_view(['GET',])
def getMyProfile(request, email):

    try:
        email = profile.objects.filter(email=email)
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfileAPI(email,many=True)
        return Response(serializer.data)

@api_view(['PUT',])
def updateMyProfile(request, email):

    try:
        email = profile.objects.filter(email=email).first()
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfileAPI(email, data=request.data)
        info = {}
        if serializer.is_valid():
            serializer.save()
            info['response'] = "Profile updated."
        else:
            info = serializer.errors
        return Response(info)  

#view_generic_posts
@api_view(['GET','POST',])
def genericPosts(request):
    #content_feed_fetching
    queryset = models.posts.objects.all()
    if request.method == 'GET':
        serializer = contentfeedSerializer(queryset, many=True)
        return Response(serializer.data)
        
    #content_feed_inserting
    elif request.method == 'POST':
        serializer = contentfeedSerializer(data=request.data)
        contentinfo = {}
        if serializer.is_valid():
            contentdata = serializer.save()
            contentinfo['response'] = "Content feeded."
            contentinfo['description'] = contentdata.description
            contentinfo['post_time'] = contentdata.post_time
            contentinfo['post_id'] = contentdata.post_id
            contentinfo['username'] = contentdata.username.username
            return Response(contentinfo)  
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

#My_Post_ GET
@api_view(['GET',])
def get_myPost(request, username):
    try:
        myPost = posts.objects.filter(username=username)
    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = contentfeedSerializer(myPost,many=True)
        return Response(serializer.data)
    # return Response(serializer.errors, status=HTTP_204_NO_CONTENT)

@api_view(['DELETE',])
def delete_mypost(request,post_id):
    try:
        post = models.posts.objects.get(post_id=post_id)
    except models.posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #POST DELETE 
    if request.method == 'DELETE':
        deleted_post = post.delete()
    return Response("Post not exist",status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT',])
def update_myPost(request, post_id):
    try:
        myPost = posts.objects.get(post_id=post_id)
    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PostsSerializerWithoutPostId(myPost, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Updated successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

# #Get_Count_Of_Users ---------------------------------- working status
@api_view(['GET',])
def no_of_users_registerd(request):
    if request.method == 'GET':
        total_users = account.objects.count()
        return Response(int(total_users))

#female
@api_view(['GET',])
def no_of_females(request):
    if request.method == 'GET':
        total_users = profile.objects.filter(gender='f').count()
        return Response(int(total_users))

#male
@api_view(['GET',])
def no_of_males(request):
    if request.method == 'GET':
        total_users = profile.objects.filter(gender='m').count()
        return Response(int(total_users))
