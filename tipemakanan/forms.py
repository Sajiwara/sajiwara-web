from django import forms
from .models import Makanan

class PreferensiForm(forms.Form):
    preferensi = forms.ChoiceField(
        choices=[('', 'Pilih negara')],
        label="Pilih Preferensi Negara",
        required=True
        # widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(PreferensiForm, self).__init__(*args, **kwargs)
        # Mengambil preferensi unik dari model Makanan untuk form
        self.fields['preferensi'].choices += [(m, m) for m in Makanan.objects.values_list('preferensi', flat=True).distinct()]

class MakananUpdateForm(forms.ModelForm):
    class Meta:
        model = Makanan
        fields = ['preferensi', 'menu', 'restoran']  # Fields yang bisa diubah oleh user
        labels = {
            'preferensi': 'Preferensi Negara',
            'menu': 'Variasi Makanan',
            'restoran': 'Nama Restoran',
        }
        widgets = {
            'preferensi': forms.TextInput(attrs={'class': 'form-control'}),
            'menu': forms.TextInput(attrs={'class': 'form-control'}),
            'restoran': forms.TextInput(attrs={'class': 'form-control'}),
        }