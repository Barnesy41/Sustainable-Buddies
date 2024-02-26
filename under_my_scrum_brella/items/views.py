from django.shortcuts import get_object_or_404, render, redirect

from users.models import UserDetail
from .models import Item, UserItem
from django.contrib import messages

# Create your views here.
def shop(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    if request.method == 'POST':
        itemId = request.POST["id"]
        currentUser = request.user
        selectedItem = Item.objects.get(itemID=itemId)
        if not selectedItem:
            messages.success(request, "Item Not Found")
            return redirect('shop')
        user_details = get_object_or_404(UserDetail, pk=currentUser.id)
        if user_details.total_coins < selectedItem.item_cost:
            messages.success(request, "Insufficient Funds")
            return redirect('shop')
        try:
            userItem = UserItem(user=currentUser, item=selectedItem)
            userItem.save()
            UserDetail.objects.filter(user=currentUser).update(total_coins = user_details.total_coins - selectedItem.item_cost)
            messages.success(request, "Item Successfully Purchased")
        except:
            messages.success(request, "Item Already Purchased")
        return redirect('shop')
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