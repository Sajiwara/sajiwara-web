from django import forms
from .models import WishlistMenu, Menu

class WishlistMenuForm(forms.ModelForm):
    menu = forms.ModelChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Menu"
    )

    class Meta:
        model = WishlistMenu
        fields = ['menu']
