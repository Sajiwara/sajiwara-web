from django.forms import ModelForm
from search.models import Restaurant

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["nama", "jenis", "rating", "harga", "jarak"]