from django import forms
from .models import Makanan

class PreferensiForm(forms.Form):
    preferensi = forms.ChoiceField(
        choices=[],
        label="Pilih Preferensi Negara",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(PreferensiForm, self).__init__(*args, **kwargs)
        # Mengambil preferensi unik dari model Makanan untuk form
        self.fields['preferensi'].choices = [(m, m) for m in Makanan.objects.values_list('preferensi', flat=True).distinct()]