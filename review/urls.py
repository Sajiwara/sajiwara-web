from django.urls import path
from . import views  # Import your views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('restaurant/<uuid:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('add_review/<uuid:id>/', views.add_review, name='add_review'),
    path('delete/<uuid:id>/', views.delete_review, name='delete_review'),
    path('edit/<uuid:id>/', views.edit_review, name='edit_review'),
    path('jsonResto/', views.show_json_restoran, name='show_json_restoran'),
    path('<uuid:id>/jsonReview/', views.show_json_review, name='show_json_review'),
    path('create-flutter/', views.create_review_flutter, name='create_review_flutter'),



]