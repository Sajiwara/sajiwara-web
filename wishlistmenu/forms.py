from django import forms
from .models import WishlistMenu, Menu

class WishlistMenuForm(forms.ModelForm):
    menu = forms.ModelChoiceField(
        queryset=Menu.objects.all(), # Mengambil semua instance dari model Menu sebagai pilihan
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Menu" # Label yang akan muncul pada form untuk field menu
    )

    class Meta:
        model = WishlistMenu
        fields = ['menu']
