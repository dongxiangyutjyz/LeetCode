from django.contrib import admin
from .models import Twitter_User, Tweet
# Register your models here.

admin.site.register(Twitter_User)

admin.site.register(Tweet)