from django.contrib import admin

from .models import Item, UserItem
# Register your models here.
admin.site.register(Item)
admin.site.register(UserItem)