from django.urls import path
from wishlistresto.views import show_wishlistresto
from tipemakanan.views import makanan_list
from landingpage.views import show_landingpage,login,logout,register
from search.views import show_search

app_name = 'landingpage'

urlpatterns = [
    path('', show_landingpage, name='show_landingpage'),
    path('search/', show_search, name='show_search'),
    # path('explore/', views.explore, name='explore'),
    path('wishlistresto/', show_wishlistresto, name='show_wishlistresto'),
    path('makanan/', makanan_list, name='makanan_list'),
    # path('add_review/', views.add_review, name='add_review'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]