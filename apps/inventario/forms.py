from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ['creado_en', 'actualizado_en', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 2})}
