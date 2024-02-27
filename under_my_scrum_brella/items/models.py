  ###########################################################################
  #   Author: Silas Turner 
  #   Contributors: Oliver Fitzgerald
  #
  #   The author has written all code in this file unless stated otherwise.
  ###########################################################################


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(max_length=400)
    item_cost = models.IntegerField(default=100)
    item_location = models.CharField(max_length=255)
    # index used for displaying item 
    item_index = models.IntegerField(default=0)

# Oliver Fitzgerald 
class UserItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_worn = models.BooleanField(default=False)
    class Meta:
        unique_together = ["user", "item"]