from django.urls import path
from authentication.views import *
app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('is-anonymous/', check_is_anonymous, name='check_is_anonymous'),
    path('get-user-data/', get_user_data, name='get_user_data'),
]