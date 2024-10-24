from django.urls import path
from . import views  # Import your views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('add_review/<int:restaurant_id>/', views.add_review, name='add_review'),
    path('delete/<int:review_id>', views.delete_review, name='delete_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
]