###########################################################################
#   Author: Silas Turner
#   Contributors: Ollie Barnes, Ellie Andrews, Jack Bundy, Luke Clarke
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserDetail, Friend
from .models import UserDetail


# Create your views here.
def login_user(request):
    if request.method == 'POST': #Branch for post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #Try to authenticate the user
        if user is not None: #If user exists login
            login(request, user)
            return redirect('home')
        else: # Else send the user a message
            messages.success(request, "Error logging in try again")
            return redirect('login')
    else: #Branch for get
        user = request.user
        if user.is_authenticated: #If user is logged in add user details to context
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context = {'user_details': user_details}
            return render(request, 'login.html', context)
        else:
            return render(request, 'login.html')

def signup_user(request):
    if request.method == 'POST': #Branch for post
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        new_buddy_name = request.POST['buddyName']
        new_buddy_type = request.POST['buddyType']
        try: #Try and create a new user
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            userdetail = UserDetail(user=new_user, buddy_name=new_buddy_name, buddy_type=new_buddy_type)
            userdetail.save()
        except: #If fails then user already exists
            messages.success(request, "Username taken try again")
            return redirect('signup')

        auth_user = authenticate(request, username=username, password=password) #Authenticate the user and redirect
        if auth_user is not None:
            login(request, auth_user)
            return redirect('home')
        else:
            messages.success(request, "Error signing up try again")
            return redirect('signup')
    else: #Branch for get
        user = request.user
        if user.is_authenticated: #If user is logged in add user details to context
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context = {'user_details': user_details}
            return render(request, 'signup.html', context)
        else:
            return render(request, 'signup.html')

def logout_user(request):
    logout(request) #Logout the user
    messages.success(request, "Successfully logged out")
    return redirect('home')

def friends(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')
    if request.user.is_superuser: #Check if user is superuser
        return redirect('/admin/')
    if request.method == 'POST': #Branch for post
        if "accept" in request.POST: #If accept button is clicked, update friend record
            Friend.objects.filter(id=request.POST["id"]).update(pending_first_second = False, pending_second_first = False, friends = True)
            messages.success(request, "Successfully added friend")
            return redirect('friends')
        elif "decline" in request.POST: #If decline button is clicked, delete friend record
            Friend.objects.filter(id=request.POST["id"]).delete()
            messages.success(request, "Deleted friend request")
            return redirect('friends')
        else: #If add friend button is clicked
            user = request.user
            new_friend_maybe = User.objects.filter(username=request.POST["friend_username"])
            if not new_friend_maybe: #Check to see if user exists
                messages.success(request, "Username Not Found")
                return redirect('friends')
            new_friend = new_friend_maybe[0]
            try: #Try and add friend
                if user.id < new_friend.id:
                    friendship = Friend(user1=user, user2=new_friend, pending_first_second=True, pending_second_first=False, friends=False)
                    friendship.save()
                elif user.id == new_friend.id: #Catch for if friend is yourself
                    messages.success(request, "Cannot add yourself as a friend")
                    return redirect('friends')
                else:
                    friendship = Friend(user1=new_friend, user2=user, pending_first_second=False, pending_second_first=True, friends=False)
                    friendship.save()
                messages.success(request, "Sent Friend Request")
            except: #Catch for if friend already exists
                messages.success(request, "This user is either already your friend or you have ongoing friend requests")
            return redirect('friends')
    else: #Branch for get
        friends1 = Friend.objects.select_related("user2").filter(user1=request.user).filter(friends=True) #Get Friends
        friends2 = Friend.objects.select_related("user1").filter(user2=request.user).filter(friends=True)
        friends = [] #Format the friends
        for friend in friends1:
            friends.append(friend.user2)
        for friend in friends2:
            friends.append(friend.user1)
        context = {'friends': friends}
        #Get friend requests
        friend_requests1 = Friend.objects.select_related("user2").filter(user1=request.user).filter(pending_second_first=True)
        friend_requests2 = Friend.objects.select_related("user1").filter(user2=request.user).filter(pending_first_second=True)
        friend_requests = [] #Format friend requests
        for friend_request in friend_requests1:
            new_request = friend_request.user2
            new_request.friend_id = friend_request.id
            friend_requests.append(new_request)
        for friend_request in friend_requests2:
            new_request = friend_request.user1
            new_request.friend_id = friend_request.id
            friend_requests.append(new_request)
        context['friend_requests'] = friend_requests
        user = request.user #If user is logged in add user details to context
        if user.is_authenticated:
            user_details = get_object_or_404(UserDetail, pk=user.id)
            context['user_details'] = user_details
            return render(request, 'friends.html', context)
        else:
            return render(request, 'friends.html', context)

# Made by jack
def account(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


    user_details = get_object_or_404(UserDetail, pk=request.user.id)

    # If they try to edit a pass/email:
    # ^^ Even if activated when from someone elses it would only change their own
    # Even though you should not be able to anyway
    context = {
        'user_details': user_details, 
        'viewed_user': user_details, 
    }
    if request.method == "POST":
        if "changePass" in request.POST:
            old_pass = request.POST["old_pass"]
            new_pass = request.POST["new_pass"]
            repeat_pass = request.POST["new_pass_repeat"]

            if authenticate(request, username=user_details.user.username, password=old_pass) is not None:
                if new_pass == repeat_pass:
                    user_details.user.set_password(new_pass)
                    user_details.user.save()
                    messages.success(request, "Password changed")
                    # Password changes log out, hence re-auth
                    login(request, authenticate(request, username=user_details.user.username, password=new_pass))
                else:
                    messages.success(request, "Passwords did not match")
            else:
                messages.success(request, "Incorrect password")

        elif "changeMail" in request.POST:
            user_details.user.email = request.POST["new_email"]
            user_details.user.save()
            user_details = get_object_or_404(UserDetail, pk=request.user.id)
        context = {
            'user_details': user_details, 
            'viewed_user': user_details, 
        }

    # View of someone elses account
    elif request.method == "GET" and 'userId' in request.GET:
        viewed_user = get_object_or_404(UserDetail, pk=request.GET["userId"])
        # Overrides the default from above
        context = {
            'user_details': user_details, 
            'viewed_user': viewed_user,
        }

    # It is a regular page view of the account owner
    return render(request, 'account.html', context)
    
        
# The leaderboard function below was written by Ollie Barnes & Ellie Andrews
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
    friends.append(User.objects.get(id=currentUser.id))   #Add the current user to the list to ensure they show in the friends leaderboard
    
    #Calculate the total xp for each friend
    for friend in friends:
        friend.total_xp = UserDetail.objects.get(user=friend).total_xp
    
    # Sort the friend list by total xp
    friends.sort(key=lambda x: x.total_xp, reverse=True)
    context = {'friends': friends}
    
    #Get a list of all the Users signed up to the website & sort by XP level
    all_users = UserDetail.objects.all()
    sorted_xp_all_users = all_users.order_by('-total_xp')   #Order by descending XP level
    context['all_users'] = sorted_xp_all_users

    #Return all the details of the user, allowing their coins to show on the nav bar
    user_details = get_object_or_404(UserDetail, pk=currentUser.id)
    context['user_details'] = user_details
    
    return render(request, 'leaderboard.html', context)

#Ellie Andrews
def social(request):
    if not request.user.is_authenticated: #Check if user is logged in
        messages.success(request, "Please login first")
        return redirect('login')
    else:
        return render(request, 'social.html')

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

        user_details.save()

#Luke Clarke - checks whether happiness should decay
def decayHappiness(request):
    secondsToDecay = 3600 #how many seconds until happiness decays
    decayPerIncrement = 0.05 #how much happiness decays by

    currentUser = request.user

    if currentUser.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=currentUser.id)
        
        current_time = timezone.now()
        time_elapsed = (current_time - user_details.last_happiness_decay_time).total_seconds()

        time_segments_elapsed = time_elapsed/secondsToDecay
        decayValue = time_segments_elapsed * decayPerIncrement

        #decays happiness after set time has passed
        if (time_elapsed > secondsToDecay):
            updateHappiness(currentUser, -decayValue)
            user_details.last_happiness_decay_time = current_time
            