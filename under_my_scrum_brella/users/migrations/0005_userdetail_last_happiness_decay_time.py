# Generated by Django 5.0.3 on 2024-03-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_userdetail_buddy_happiness"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdetail",
            name="last_happiness_decay_time",
            field=models.DateTimeField(auto_now=True),
        ),
    ]