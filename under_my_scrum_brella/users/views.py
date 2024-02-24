from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserDetail, Item

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Error logging in try again")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        new_buddy_name = request.POST['buddyName']
        new_buddy_type = request.POST['buddyType']
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            userdetail = UserDetail(user=new_user, buddy_name=new_buddy_name, buddy_type=new_buddy_type)
            userdetail.save()
        except:
            messages.success(request, "Username taken try again")
            return redirect('signup')

        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return redirect('home')
        else:
            messages.success(request, "Error signing up try again")
            return redirect('signup')
    else:
        return render(request, 'signup.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')