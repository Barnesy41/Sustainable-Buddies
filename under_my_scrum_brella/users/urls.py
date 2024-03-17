###########################################################################
#   Author: Silas Turner
#   Contributors: Ollie Barnes, Ellie Andrews
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('friends/', views.friends, name='friends'),
    path('account/', views.account, name='account'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('social/', views.social, name='social')
]