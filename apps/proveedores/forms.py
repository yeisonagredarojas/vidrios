from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['creado_en', 'activo']
        widgets = {'notas': forms.Textarea(attrs={'rows': 2})}
