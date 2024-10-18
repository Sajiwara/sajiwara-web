from django import forms

class SearchRestoForm(forms.Form):
    query = forms.CharField(label='Nama Restoran', max_length=266)
