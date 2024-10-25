from django.urls import path
from . import views
from wishlistmenu.views import add_to_wishlist, wishlist_page, mark_as_tried, delete_wishlist_item

app_name = 'wishlistmenu'

urlpatterns = [
    path('add-to-wishlist/<uuid:id>', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/<uuid:id>', wishlist_page, name='wishlist_page'),
    path('mark-as-tried/<uuid:id>/', mark_as_tried, name='mark_as_tried'),
    path('delete-wishlist-item/<uuid:id>/', delete_wishlist_item, name='delete_wishlist_item'),
]
