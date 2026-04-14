from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude = ['area_calculada', 'precio_total', 'fecha']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'notas_internas': forms.Textarea(attrs={'rows': 2}),
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('cliente', css_class='col-md-8'), Column('estado', css_class='col-md-4')),
            Row(Column('tipo_vidrio', css_class='col-md-4'), Column('tipo_trabajo', css_class='col-md-4'), Column('trabajador_asignado', css_class='col-md-4')),
            Row(Column('ancho', css_class='col-md-4'), Column('alto', css_class='col-md-4'),
                Column(HTML('<div class="mb-3"><label class="form-label">Área calculada</label><div id="area_display" class="form-control bg-light">0.00 m²</div></div>'), css_class='col-md-4')),
            HTML('<div id="precio_display" class="alert alert-info d-none"><strong>Precio estimado: <span id="precio_valor">$0</span></strong></div>'),
            Row(Column('ciudad_entrega', css_class='col-md-8'), Column('es_envio_nacional', css_class='col-md-4 mt-4')),
            'direccion_entrega', 'descripcion', 'imagen',
            Row(Column('fecha_entrega_estimada', css_class='col-md-6'), Column('notas_internas', css_class='col-md-6')),
            Submit('submit', 'Guardar Pedido', css_class='btn btn-success btn-lg')
        )
