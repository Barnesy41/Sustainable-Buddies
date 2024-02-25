from django.shortcuts import get_object_or_404, render

from users.models import UserDetail, Item

def home(request):
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
    
def my_pet(request):
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'mypet.html', context)
    else:
        return render(request, 'mypet.html')
    
def shop(request):
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context = {'user_details': user_details}
        return render(request, 'shop.html', context)
    else:
        return render(request, 'shop.html')
    
def wardrobe(request):
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