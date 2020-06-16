"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


from signup.api.views import register
from signup.api.views import createAPIView
from rest_framework.authtoken import views
from signup.api.views import profileView
# from signup.api.views import PostDeleteAPIView
#content_feed_view

from rest_framework import routers
from signup.api.views import content_feed,content_feed_pk
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('profile', profileView, name='profileView'),
    path('login', createAPIView.as_view(), name='login'),
    path('posts' ,content_feed, name="content_feed"),
    path('posts/<post_id>',content_feed_pk, name="content_feed_pk"),
    # path('posts/:pk',content_feed_details, name="content_feed_details"),
    # path('(?P<description>[\w-]+)/delete/',PostDeleteAPIView.as_view(), name='delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)