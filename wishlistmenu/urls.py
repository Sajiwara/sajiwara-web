from django.urls import path
from wishlistmenu.views import show_wishlistmenu, add_to_wishlist, tried_menu, delete_wishlist,not_tried_menu

app_name = 'wishlistmenu'

urlpatterns = [
     path('', show_wishlistmenu, name='show_wishlistmenu'),
     path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
     path('visited/<uuid:id>/', tried_menu, name='tried_menu'),
     path('notvisited/<uuid:id>/', not_tried_menu, name='not_tried_menu'),
     path('deletewishlist/<uuid:id>/', delete_wishlist, name='delete_wishlist'),
]