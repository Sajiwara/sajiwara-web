# from django import forms

# class SearchRestoForm(forms.Form):
#     query = forms.CharField(label='Nama Restoran', max_length=266)

from django import forms
from .models import Resto

# class SearchRestoForm(forms.Form):
#     # restaurant_ids = forms.ModelMultipleChoiceField(
#     #     queryset=Resto.objects.all(),
#     #     widget=forms.CheckboxSelectMultiple,
#     #     label="Pilih Restoran"
#     # )
#     query = forms.CharField(label='Pilih Restoran', max_length=266)

from django import forms
from django.forms import ModelForm
from wishlistresto.models import Resto

class SearchRestoForm(ModelForm):
    class Meta:
        model = Resto
        fields = ["restaurant"]

    restaurant = forms.ModelChoiceField(
        queryset=Resto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional: Styling with Bootstrap
        empty_label="Select a restaurant"
    )