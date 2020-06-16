from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(account)
admin.site.register(profile)
admin.site.register(posts)