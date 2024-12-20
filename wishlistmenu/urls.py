from django.urls import path
from wishlistmenu.views import *;

app_name = 'wishlistmenu' 

urlpatterns = [
     path('', show_wishlistmenu, name='show_wishlistmenu'),
     path('menus/', show_menus, name='show_menus'),
     path('restaurants/', show_restaurants, name='show_restaurants'),
     path('add-to-wishlistmenu/', add_to_wishlistmenu, name='add_to_wishlistmenu'),
     path('visited/<uuid:id>/', tried_menu, name='tried_menu'),
     path('notvisited/<uuid:id>/', not_tried_menu, name='not_tried_menu'),
     path('deletewishlist/<uuid:id>/', delete_wishlist, name='delete_wishlist'),
     path('json/', show_json, name='show_json'),
     path('add-to-wishlist-flutter/', add_to_wishlist_flutter, name='add_to_wishlist_flutter'),
     path('visited-flutter/<uuid:id>/', tried_menu_flutter, name='tried_menu_flutter'),
     path('deletewishlist-flutter/<uuid:id>/', delete_wishlist_flutter, name='delete_wishlist_flutter'),
]