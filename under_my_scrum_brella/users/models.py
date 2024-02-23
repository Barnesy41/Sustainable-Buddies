from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    buddy_name = models.CharField(max_length=400)
    buddy_type = models.CharField(max_length=400)
    total_coins = models.IntegerField(default=0)
    total_xp = models.IntegerField(default=0)