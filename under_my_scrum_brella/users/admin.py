from django.contrib import admin

from .models import UserDetail, Friend

admin.site.register(UserDetail)
admin.site.register(Friend)