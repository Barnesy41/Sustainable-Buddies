# Generated by Django 5.1.dev20240130101038 on 2024-03-17 15:53

from django.db import migrations

def populate_items_new(apps, schema_editor):
    Item = apps.get_model('items', 'Item')
    Item.objects.create(item_name="Party Hat", item_location="partyhatitem.png", item_description="It is time to party!", item_cost=600, item_index=5)
    Item.objects.create(item_name="Picnic Basket", item_location="picnicbasketitem.png", item_description="Some people like eating on the floor!", item_cost=250, item_index=6)
    Item.objects.create(item_name="Teddy Bear", item_location="teddybearitem.png", item_description="A little buddy for your buddy!", item_cost=800, item_index=7)
    Item.objects.create(item_name="Dress", item_location="dressitem.png", item_description="A lovely dress!", item_cost=400, item_index=8)
    Item.objects.create(item_name="Formal Suit", item_location="suititem.png", item_description="Perfect for a sophisticated buddy!", item_cost=1000, item_index=9)
    

class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20240227_1033'),
    ]

    operations = [
        migrations.RunPython(populate_items_new),
    ]
