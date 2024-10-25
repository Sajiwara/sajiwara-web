from django.urls import path
from .views import makanan_list, edit_makanan

app_name = 'tipemakanan'

urlpatterns = [
    path('', makanan_list, name='makanan_list'),
    path('edit/<int:pk>/', edit_makanan, name='edit_makanan'),
]