from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']  # Fields to include in the form

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Cari Restoran')