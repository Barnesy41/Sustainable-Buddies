# Generated by Django 5.0.2 on 2024-02-23 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('buddy_name', models.CharField(max_length=400)),
                ('buddy_type', models.CharField(max_length=400)),
                ('total_coins', models.IntegerField(default=0)),
                ('total_xp', models.IntegerField(default=0)),
            ],
        ),
    ]
