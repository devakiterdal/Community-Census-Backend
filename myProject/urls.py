from django.contrib import admin
from django.urls import path,include

from signup.api.views import register
from rest_framework.authtoken import views
from rest_framework import routers
from signup.api.views import genericPosts, delete_mypost, get_myPost, login, update_myPost, getMyProfile,no_of_males,no_of_females, updateMyProfile, no_of_users_registerd
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('posts' ,genericPosts, name="genericPosts"),
    path('delete/<post_id>',delete_mypost, name="delete_mypost"),
    path('update/<post_id>',update_myPost, name="update"),
    path('my-posts/<username>', get_myPost, name='myPost'),
    path('my-profile/<email>', getMyProfile, name='getMyProfile'),
    path('update-my-profile/<email>', updateMyProfile, name='updateMyProfile'),
    path('total-users-registerd', no_of_users_registerd, name='totalregisteredusers'),
    path('total-female', no_of_females, name='totalregisteredusers'),
    path('total-male', no_of_males, name='totalregisteredusers'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)