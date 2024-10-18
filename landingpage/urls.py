from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.show_landingpage, name='show_landingpage'),
    path('search/', views.search, name='search'),
    path('explore/', views.explore, name='explore'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('add_review/', views.add_review, name='add_review'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
]