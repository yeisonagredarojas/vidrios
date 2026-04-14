from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'direccion', 'ciudad', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('nombre', css_class='col-md-8'), Column('telefono', css_class='col-md-4')),
            Row(Column('correo', css_class='col-md-6'), Column('ciudad', css_class='col-md-6')),
            'direccion', 'notas',
            Submit('submit', 'Guardar Cliente', css_class='btn btn-primary btn-lg')
        )
