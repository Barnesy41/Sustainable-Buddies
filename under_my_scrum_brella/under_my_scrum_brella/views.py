from django.shortcuts import render
from users.models import Item

def wardrobe(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'wardrobe.html', context)
