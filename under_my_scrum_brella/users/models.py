from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    buddy_name = models.CharField(max_length=400)
    buddy_type = models.CharField(max_length=400)
    total_coins = models.IntegerField(default=0)
    total_xp = models.IntegerField(default=0)

class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')
    pending_first_second= models.BooleanField()
    pending_second_first= models.BooleanField()
    friends = models.BooleanField(default=False)
    class Meta:
        unique_together = ["user1", "user2"]

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(max_length=400)
    item_cost = models.IntegerField(default=100)