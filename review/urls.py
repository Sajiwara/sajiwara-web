from django.urls import path
from . import views  # Import your views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),

]