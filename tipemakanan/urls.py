from django.urls import path
from .views import makanan_list

app_name = 'tipemakanan'

urlpatterns = [
    path('', makanan_list, name='makanan_list'),
]