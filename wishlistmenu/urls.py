from django.urls import path
from wishlistmenu.views import show_wishlistmenu, show_menus, show_restaurants, add_to_wishlistmenu, tried_menu, delete_wishlist, not_tried_menu 
from wishlistmenu.views import (
    show_wishlistmenu_api,
    show_menus_api,
    show_restaurants_api,
    add_wishlistmenu_api,
    update_tried_status_api,
    delete_wishlist_api,
    show_json_api,
    get_json_menu_data_api,
    show_triedmenu_api

)
app_name = 'wishlistmenu' 

urlpatterns = [
    path('', show_wishlistmenu, name='show_wishlistmenu'),
    path('restaurants', show_restaurants, name='show_restaurants'),
    path('menus', show_menus, name='show_menus'),
    path('add-to-wishlist/', add_to_wishlistmenu, name='add_to_wishlistmenu'),
    path('tried/<uuid:id>/', tried_menu, name='tried_menu'),
    path('nottried/<uuid:id>/', not_tried_menu, name='not_tried_menu'),
    path('delete/<uuid:id>/', delete_wishlist, name='delete_wishlist'),

    path('api/wishlist/', show_wishlistmenu_api, name='show_wishlistmenu_api'),
    path('api/menus/', show_menus_api, name='show_menus_api'),
    path('api/restaurants/', show_restaurants_api, name='show_restaurants_api'),
    path('api/add-to-wishlist/', add_wishlistmenu_api, name='add_wishlistmenu_api'),
    path('api/tried/', show_triedmenu_api, name='show_triedmenu_api'),
    path('api/update-tried/<uuid:id>/', update_tried_status_api, name='update_tried_status_api'),
    path('api/delete-wishlist/<uuid:id>/', delete_wishlist_api, name='delete_wishlist_api'),
    path('api/wishlist-json/', show_json_api, name='show_json_api'),
    path('api/menu-json/', get_json_menu_data_api, name='get_json_menu_data_api'),
]