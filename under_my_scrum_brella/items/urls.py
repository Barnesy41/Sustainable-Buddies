from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('wardrobe/', views.wardrobe, name='wardrobe')
]