from django.urls import path
from wishlistmenu.views import show_wishlistmenu, show_menus, show_restaurants, add_to_wishlistmenu, tried_menu, delete_wishlist, not_tried_menu

app_name = 'wishlistmenu' 

urlpatterns = [
    path('', show_wishlistmenu, name='show_wishlistmenu'),
    path('restaurants', show_restaurants, name='show_restaurants'),
    path('menus', show_menus, name='show_menus'),
    path('add-to-wishlist/', add_to_wishlistmenu, name='add_to_wishlistmenu'),
    path('tried/<uuid:id>/', tried_menu, name='tried_menu'),
    path('nottried/<uuid:id>/', not_tried_menu, name='not_tried_menu'),
    path('delete/<uuid:id>/', delete_wishlist, name='delete_wishlist'),
]
