from django.urls import path
from wishlistresto.views import show_wishlistresto, add_to_wishlist, visited_resto, delete_wishlist,not_visited_resto, show_json, add_to_wishlist_flutter

app_name = 'wishlistresto'

urlpatterns = [
     path('', show_wishlistresto, name='show_wishlistresto'),
     path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
     path('visited/<uuid:id>/', visited_resto, name='visited_resto'),
     path('notvisited/<uuid:id>/', not_visited_resto, name='not_visited_resto'),
     path('deletewishlist/<uuid:id>/', delete_wishlist, name='delete_wishlist'),
     path('json/', show_json, name='show_json'),
     path('add-to-wishlist-flutter/', add_to_wishlist_flutter, name='add_to_wishlist_flutter'),
]
