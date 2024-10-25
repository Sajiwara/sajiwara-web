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
            'menu': forms.Textarea(attrs={
                'rows': 5,  # Atur tinggi box dengan jumlah baris
                'cols': 50,  # Atur lebar box
                'class': 'form-control',
            }),
            'preferensi': forms.Textarea(attrs={
                'rows': 1,  # Atur tinggi box dengan jumlah baris
                'cols': 25,  # Atur lebar box
                'class': 'form-control',
            }),
            'restoran': forms.Textarea(attrs={
                'rows': 1,  # Atur tinggi box dengan jumlah baris
                'cols': 50,  # Atur lebar box
                'class': 'form-control',
            }),
        }
        def __init__(self, *args, **kwargs):
            super(MakananUpdateForm, self).__init__(*args, **kwargs)
            # Membuat 'restoran' dan 'preferensi' menjadi readonly
            self.fields['restoran'].widget.attrs['readonly'] = True
            self.fields['preferensi'].widget.attrs['readonly'] = True