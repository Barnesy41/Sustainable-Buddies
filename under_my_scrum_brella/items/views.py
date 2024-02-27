from django.shortcuts import get_object_or_404, render, redirect

from users.models import UserDetail
from .models import Item, UserItem
from django.contrib import messages

# Create your views here.
def shop(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser:
        return redirect('/admin/')
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

    if request.user.is_superuser:
        return redirect('/admin/')

    user = request.user
 
    if request.method == 'POST':
        UserItem.objects.filter(user=user).update(is_worn=False)
        selected_indices_str = request.POST.get('selected_indices', '')
        item_array = [int(index) for index in selected_indices_str.split(',') if index.isdigit()]
        for number in item_array:   
            item_to_update = Item.objects.get(item_index=number)
            user_item, created = UserItem.objects.get_or_create(user=user, item=item_to_update)
            # Set is_worn to True
            user_item.is_worn = True
            user_item.save()


   
    if user.is_authenticated:

        user_details = get_object_or_404(UserDetail, pk=user.id)
        # ollie f - added access to items for wardrobe
        all_items = Item.objects.all()
        # Get all UserItem instances where is_worn is True
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        # Extract item_index values and store in an array
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        item_array = []
        #all_items = []
        #user_items = UserItem.objects.filter(user=user)
        #for user_item in user_items:
            #all_items.append(user_item.item)
        context = {
            'user_details': user_details,
            'all_items': all_items,
            'item_array':item_array,
            'index_array':index_array,
            }
        return render(request, 'wardrobe.html', context)
    else:
        return render(request, 'wardrobe.html')