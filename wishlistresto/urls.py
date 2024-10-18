from django.urls import path
from wishlistresto.views import show_wishlist

app_name = 'wishlistresto'

urlpatterns = [
     path('', show_wishlist, name='show_wishlist'),
]
