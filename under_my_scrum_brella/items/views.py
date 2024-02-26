from django.shortcuts import get_object_or_404, render, redirect

from users.models import UserDetail
from .models import Item
from django.contrib import messages

# Create your views here.
def shop(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # ellie - added access to items for shop
        all_items = Item.objects.all()
        context = {
            'user_details': user_details,
            'all_items': all_items,
            }
        return render(request, 'shop.html', context)
    else:
        return render(request, 'shop.html')
    
def wardrobe(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # ollie f - added access to items for wardrobe
        all_items = Item.objects.all()
        context = {
            'user_details': user_details,
            'all_items': all_items,
            }
        return render(request, 'wardrobe.html', context)
    else:
        return render(request, 'wardrobe.html')