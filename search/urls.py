from django.urls import path
from search.views import show_search,show_xml,show_json,show_json_by_id,show_xml_by_id

app_name = 'search'

urlpatterns = [
    path('', show_search, name='show_search'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
   
]   