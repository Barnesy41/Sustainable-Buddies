  ###########################################################################
  #   Author: Silas Turner 
  #   Contributors:
  #
  #   The author has written all code in this file unless stated otherwise.
  ###########################################################################
from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('wardrobe/', views.wardrobe, name='wardrobe')
]