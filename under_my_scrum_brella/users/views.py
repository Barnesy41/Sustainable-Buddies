from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserDetail, Friend
from .models import UserDetail


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
        user = request.user
        if user.is_authenticated:
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context = {'user_details': user_details}
            return render(request, 'login.html', context)
        else:
            return render(request, 'login.html')

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
        user = request.user
        if user.is_authenticated:
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context = {'user_details': user_details}
            return render(request, 'signup.html', context)
        else:
            return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def friends(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser:
        return redirect('/admin/')
    if request.method == 'POST':
        if "accept" in request.POST:
            Friend.objects.filter(id=request.POST["id"]).update(pending_first_second = False, pending_second_first = False, friends = True)
            messages.success(request, "Successfully added friend")
            return redirect('friends')
        elif "decline" in request.POST:
            Friend.objects.filter(id=request.POST["id"]).delete()
            messages.success(request, "Deleted friend request")
            return redirect('friends')
        else:
            user = request.user
            new_friend_maybe = User.objects.filter(username=request.POST["friend_username"])
            if not new_friend_maybe:
                messages.success(request, "Username Not Found")
                return redirect('friends')
            new_friend = new_friend_maybe[0]
            try:
                if user.id < new_friend.id:
                    friendship = Friend(user1=user, user2=new_friend, pending_first_second=True, pending_second_first=False, friends=False)
                    friendship.save()
                elif user.id == new_friend.id:
                    messages.success(request, "Cannot add yourself as a friend")
                    return redirect('friends')
                else:
                    friendship = Friend(user1=new_friend, user2=user, pending_first_second=False, pending_second_first=True, friends=False)
                    friendship.save()
                messages.success(request, "Sent Friend Request")
            except:
                messages.success(request, "This user is either already your friend or you have ongoing friend requests")
            return redirect('friends')
    else:
        friends1 = Friend.objects.select_related("user2").filter(user1=request.user).filter(friends=True)
        friends2 = Friend.objects.select_related("user1").filter(user2=request.user).filter(friends=True)
        friends = []
        for friend in friends1:
            friends.append(friend.user2)
        for friend in friends2:
            friends.append(friend.user1)
        context = {'friends': friends}

        friend_requests1 = Friend.objects.select_related("user2").filter(user1=request.user).filter(pending_second_first=True)
        friend_requests2 = Friend.objects.select_related("user1").filter(user2=request.user).filter(pending_first_second=True)
        friend_requests = []
        for friend_request in friend_requests1:
            new_request = friend_request.user2
            new_request.friend_id = friend_request.id
            friend_requests.append(new_request)
        for friend_request in friend_requests2:
            new_request = friend_request.user1
            new_request.friend_id = friend_request.id
            friend_requests.append(new_request)
        context['friend_requests'] = friend_requests
        user = request.user
        if user.is_authenticated:
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context['user_details'] = user_details
            return render(request, 'friends.html', context)
        else:
            return render(request, 'friends.html', context)
        
# The below code is written by Ollie Barnes & Ellie Andrews
#TODO: ensure admins arent included in the list of users?
def leaderboard(request):
    #Redirect the user to the login page if they are not signed in
    currentUser = request.user
    if not currentUser.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')

    # Get all of the friends of a user
    friends1 = Friend.objects.select_related("user2").filter(user1=currentUser).filter(friends=True)
    friends2 = Friend.objects.select_related("user1").filter(user2=currentUser).filter(friends=True)
    
    friends = []
    for friend in friends1:
        friends.append(friend.user2)
    for friend in friends2:
        friends.append(friend.user1)
    friends.append(User.objects.get(id=currentUser.id))   #Add the current user to the list
    
    #Calculate the total xp for each friend
    for friend in friends:
        friend.total_xp = UserDetail.objects.get(user=friend).total_xp
    
    # Sort the friend list by total xp
    friends.sort(key=lambda x: x.total_xp, reverse=True)
    context = {'friends': friends}
    
    #Get a list of all the Users signed up to the website & sort by XP level
    all_users = UserDetail.objects.all()
    sorted_xp_all_users = all_users.order_by('-total_xp')
    context['all_users'] = sorted_xp_all_users

    return render(request, 'leaderboard.html', context)
