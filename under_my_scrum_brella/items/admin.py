from django.contrib import admin

from .models import Item, UserItem
admin.site.register(Item)
admin.site.register(UserItem)