from django.shortcuts import get_object_or_404, redirect, render

from users.models import UserDetail

def home(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
    
def my_pet(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'mypet.html', context)
    else:
        return render(request, 'mypet.html')

def games(request):
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'games.html', context)
    else:
        return render(request, 'games.html')

def noughtsCrosses(request):
    gameCost = -1

    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        #luke - charges user when they play game
        updateCoins(user, gameCost)
        return render(request, 'Games/noughtsAndCrosses.html', context)
    else:
        return render(request, 'Games/noughtsAndCrosses.html')

#luke - used to add/subtract coins
def updateCoins(user, coinsToAdd):
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        user_details.total_coins = user_details.total_coins + coinsToAdd
        user_details.save() 
    #TODO: Add branch for if user not authenticated
        return render(request, 'mypet.html')
