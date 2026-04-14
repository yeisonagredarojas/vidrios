from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Pedido
from .forms import PedidoForm
from .services import notificar_pedido_creado, notificar_cambio_estado
from apps.cotizaciones.models import ConfiguracionPrecios
from apps.cotizaciones.services import calcular_precio


@login_required
def lista_pedidos(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    tipo = request.GET.get('tipo', '')
    qs = Pedido.objects.select_related('cliente')
    if q:
        qs = qs.filter(Q(cliente__nombre__icontains=q) | Q(pk__icontains=q))
    if estado:
        qs = qs.filter(estado=estado)
    if tipo:
        qs = qs.filter(tipo_vidrio=tipo)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'pedidos/lista.html', {
        'page_obj': page, 'q': q, 'estado': estado, 'tipo': tipo,
        'estados': Pedido.ESTADO, 'tipos': Pedido.TIPO_VIDRIO
    })


@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente', 'trabajador_asignado'), pk=pk)
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})


@login_required
def crear_pedido(request):
    config = ConfiguracionPrecios.objects.filter(activo=True).first()
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                resultado = calcular_precio({
                    'tipo_vidrio': datos['tipo_vidrio'],
                    'ancho': datos['ancho'],
                    'alto': datos['alto'],
                    'tipo_trabajo': datos['tipo_trabajo'],
                    'es_envio_nacional': datos['es_envio_nacional'],
                }, config)
                pedido = form.save(commit=False)
                pedido.precio_total = resultado['precio_total']
                pedido.save()
                notificar_pedido_creado(pedido)
                messages.success(request, f'Pedido #{pedido.pk} creado. Precio: ${pedido.precio_total:,.0f}')
                return redirect('detalle_pedido', pk=pedido.pk)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = PedidoForm()
        # Pre-llenar cliente si viene en URL
        cliente_id = request.GET.get('cliente')
        if cliente_id:
            form.initial['cliente'] = cliente_id
    return render(request, 'pedidos/form.html', {'form': form, 'titulo': 'Nuevo Pedido', 'config': config})


@login_required
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    estado_anterior = pedido.estado
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES, instance=pedido)
        if form.is_valid():
            pedido = form.save()
            if pedido.estado != estado_anterior:
                notificar_cambio_estado(pedido)
            messages.success(request, 'Pedido actualizado.')
            return redirect('detalle_pedido', pk=pk)
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/form.html', {'form': form, 'titulo': 'Editar Pedido', 'pedido': pedido})


@login_required
def calcular_precio_ajax(request):
    """Endpoint AJAX para calcular precio en tiempo real."""
    if request.method == 'POST':
        import json
        datos = json.loads(request.body)
        config = ConfiguracionPrecios.objects.filter(activo=True).first()
        if not config:
            return JsonResponse({'error': 'No hay configuración de precios activa'}, status=400)
        try:
            resultado = calcular_precio(datos, config)
            return JsonResponse({'success': True, **resultado})
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
