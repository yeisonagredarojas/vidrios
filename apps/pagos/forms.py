from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        exclude = ['registrado_por', 'creado_en']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('cliente', css_class='col-md-6'), Column('pedido', css_class='col-md-6')),
            Row(Column('monto', css_class='col-md-4'), Column('tipo_pago', css_class='col-md-4'), Column('fecha_pago', css_class='col-md-4')),
            'referencia', 'notas',
            Submit('submit', 'Registrar Pago', css_class='btn btn-success btn-lg')
        )
