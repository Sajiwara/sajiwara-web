from django.urls import path
from .views import makanan_list, edit_makanan, edit_makanan_flutter, show_xml, show_json, show_json_by_id, show_xml_by_id

app_name = 'tipemakanan'

urlpatterns = [
    path('', makanan_list, name='makanan_list'),
    path('edit/<int:pk>/', edit_makanan, name='edit_makanan'),
    path('edit-flutter/<int:pk>/', edit_makanan_flutter, name='edit_makanan_flutter'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]