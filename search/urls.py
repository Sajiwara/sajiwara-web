from django.urls import path
from search.views import show_search

app_name = 'search'

urlpatterns = [
    path('', show_search, name='show_search'),
]   