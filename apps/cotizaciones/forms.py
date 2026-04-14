from django import forms
from .models import ConfiguracionPrecios

class ConfiguracionPreciosForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionPrecios
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}
