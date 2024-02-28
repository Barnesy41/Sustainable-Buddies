  ###########################################################################
  #   Author: Silas Turner 
  #   Contributors: Oliver Fitzgerald, Ellie Andrews 
  #
  #   The author has written all code in this file unless stated otherwise.
  ###########################################################################


from django.shortcuts import get_object_or_404, render, redirect

from users.models import UserDetail
from .models import Item, UserItem
from django.contrib import messages

# Create your views here.
def shop(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')
    if request.method == 'POST': #Branch for post
        itemId = request.POST["id"]
        currentUser = request.user
        selectedItem = Item.objects.get(itemID=itemId) #Get the item
        if not selectedItem: #Check if item exists
            messages.success(request, "Item Not Found")
            return redirect('shop')
        user_details = get_object_or_404(UserDetail, pk=currentUser.id)
        if user_details.total_coins < selectedItem.item_cost: #See if the user can afford the item
            messages.success(request, "Insufficient Funds")
            return redirect('shop')
        try: #Try and buy the item
            userItem = UserItem(user=currentUser, item=selectedItem)
            userItem.save()
            UserDetail.objects.filter(user=currentUser).update(total_coins = user_details.total_coins - selectedItem.item_cost)
            messages.success(request, "Item Successfully Purchased")
        except: #Catch if user has already purchased the item
            messages.success(request, "Item Already Purchased")
        return redirect('shop')
    user = request.user
    if user.is_authenticated: #If user is logged in add user details to context
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # Ellie Andrews 
        all_items = Item.objects.all()
        context = {
            'user_details': user_details,
            'all_items': all_items,
            }
        return render(request, 'shop.html', context)
    else:
        return render(request, 'shop.html')
    
def wardrobe(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')

    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')

    user = request.user
    # Oliver Fitzgerald
    if request.method == 'POST':
        UserItem.objects.filter(user=user).update(is_worn=False)
        selected_indices_str = request.POST.get('selected_indices', '')
        item_array = [int(index) for index in selected_indices_str.split(',') if index.isdigit()]
        for number in item_array:   
            item_to_update = Item.objects.get(item_index=number)
            user_item, created = UserItem.objects.get_or_create(user=user, item=item_to_update)
            user_item.is_worn = True
            user_item.save()
        return redirect('mypet')

    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # Oliver Fitzgerald
        all_items = Item.objects.all()
        # Get all UserItem instances where is_worn is True
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        item_array = []
        # removed for now as this will be used to dynamically load items later on  
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