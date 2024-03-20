 ###########################################################################
  #   Author: Silas Turner 
  #   Contributors: Oliver Fitzgerald, Luke Clarke, Ellie Andrews
  #
  #   The author has written all code in this file unless stated otherwise.
  ###########################################################################


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

from users.models import UserDetail
from items.models import UserItem


# Global for how much happiness increases upon task completion
gameHappiness = 0.05
GAME_COST = 10

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
        decayHappiness(request)
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
        # Oliver Fitzgerald-
        worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
        index_array = [user_item.item.item_index for user_item in worn_user_items]
        # gives buddies worn items
        context = {
            'user_details': user_details,
            'index_array':index_array,
            'game_cost': GAME_COST,
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

    user = request.user
    user_details = get_object_or_404(UserDetail, pk=user.id)

    worn_user_items = UserItem.objects.filter(user=user, is_worn=True)
    index_array = [user_item.item.item_index for user_item in worn_user_items]
    
    if user_details.total_coins - GAME_COST < 0:
        messages.success(request, "Insufficient Funds")
        return redirect('games')
    updateCoins(user, -GAME_COST)
    user_details_updated = get_object_or_404(UserDetail, pk=user.id)
    context = {'user_details': user_details_updated,
               'index_array':index_array,
               }
    completeGame(user)
    return render(request, 'Games/noughtsAndCrosses.html', context)

#luke - used to add/subtract coins
def updateCoins(user, coinsToAdd):
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        user_details.total_coins = user_details.total_coins + coinsToAdd
        user_details.save()

#Ellie Andrews - loads privacy page
def privacy(request):
    user = request.user
    if user.is_authenticated: #If user is logged in add user details to context
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {
            'user_details': user_details
            }
        return render(request, 'privacy.html', context)
    else:
        return render(request, 'privacy.html')

#Ellie Andrews - adds buddy happiness for playing games with buddy
def completeGame(user_id):
    user = UserDetail.objects.get(user=user_id)
    newHappiness = max(0, min(1, user.buddy_happiness + gameHappiness))
    user.buddy_happiness = newHappiness
    user.save()


#Luke Clarke - used to update happiness and ensure it does not exceed 1
def updateHappiness(user, happinessToAdd):
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        newHappiness = user_details.buddy_happiness + happinessToAdd

        if newHappiness >= 1:
            user_details.buddy_happiness = 1
        elif newHappiness <= 0:
            user_details.buddy_happiness = 0
        else:
            user_details.buddy_happiness = newHappiness
        
        return user_details

#Luke Clarke - checks whether happiness should decay
def decayHappiness(request):
    secondsToDecay = 300 #how many seconds until happiness decays
    decayPerIncrement = 0.01 #how much happiness decays by

    currentUser = request.user

    if currentUser.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=currentUser.id)
        
        current_time = timezone.now()
        time_elapsed = (current_time - user_details.last_happiness_decay_time).total_seconds()

        #decays happiness after set time has passed
        if (time_elapsed > secondsToDecay):
            time_segments_elapsed = int(time_elapsed//secondsToDecay)
            decayValue = time_segments_elapsed * decayPerIncrement

            user_details = updateHappiness(currentUser, -decayValue)
            user_details.last_happiness_decay_time = current_time
            user_details.save()
            
