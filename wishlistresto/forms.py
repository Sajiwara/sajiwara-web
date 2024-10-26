from django import forms
from django.forms import ModelForm
from wishlistresto.models import Resto,WishlistResto
from katalog.models import Restonya

class SearchRestoForm(ModelForm):
    class Meta:
        model = WishlistResto
        fields = ["restaurant"]

    restaurant = forms.ModelChoiceField(
        queryset=Restonya.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional: Styling with Bootstrap
        empty_label="Select a restaurant"
    )