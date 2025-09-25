from django import forms
from .models import Plataforma

class PlataformaFilterForm(forms.Form):
    plataforma = forms.ModelChoiceField(
        queryset=Plataforma.objects.all(),
        required=False,
        empty_label="Todas las Plataformas",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'})
    )
