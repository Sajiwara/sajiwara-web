from django import forms
from .models import WishlistMenu

class WishlistForm(forms.ModelForm):
    class Meta:
        model = WishlistMenu
        fields = ['menu_name', 'resto_name']
        widgets = {
            'menu_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Menu'}),
            'resto_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Resto'}),
        }
