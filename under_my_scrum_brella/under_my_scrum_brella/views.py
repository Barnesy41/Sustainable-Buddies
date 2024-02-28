 ###########################################################################
  #   Author: Silas Turner 
  #   Contributors: Oliver Fitzgerald, Luke Clarke
  #
  #   The author has written all code in this file unless stated otherwise.
  ###########################################################################


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from users.models import UserDetail
from items.models import UserItem, Item

def home(request):
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')
    user = request.user
    if user.is_authenticated: #If user is logged in add user details to context
        user_details = get_object_or_404(UserDetail, pk=user.id)
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        context = {
            'user_details': user_details,
            'index_array':index_array,
            }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
    
def my_pet(request):
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')
    user = request.user
    if user.is_authenticated: #If user is logged in add user details to context
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # Oliver Fitzgerald
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        # gives all of the worn items to the mypet
        context = {
            'user_details': user_details,
            'index_array':index_array,
            }
        return render(request, 'mypet.html', context)
    else:
        return render(request, 'mypet.html')

def games(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')
    user = request.user
    if user.is_authenticated: #If user is logged in add user details to context
        user_details = get_object_or_404(UserDetail, pk=user.id)
        # Oliver Fitzgerald
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        # gives buddies worn items
        context = {
            'user_details': user_details,
            'index_array':index_array,
            }
        return render(request, 'games.html', context)
    else:
        return render(request, 'games.html')

def noughtsCrosses(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')

    gameCost = -1
    user = request.user
    user_details = get_object_or_404(UserDetail, pk=user.id)
    
    if user_details.total_coins + gameCost < 0:
        messages.success(request, "Insufficient Funds")
        return redirect('games')
    updateCoins(user, gameCost)
    user_details_updated = get_object_or_404(UserDetail, pk=user.id)
    context = {'user_details': user_details_updated}
    return render(request, 'Games/noughtsAndCrosses.html', context)

#luke - used to add/subtract coins
def updateCoins(user, coinsToAdd):
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        user_details.total_coins = user_details.total_coins + coinsToAdd
        user_details.save()