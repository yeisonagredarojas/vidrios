from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .models import Pago
from .forms import PagoForm
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido


@login_required
def lista_pagos(request):
    q = request.GET.get('q', '')
    qs = Pago.objects.select_related('cliente', 'pedido')
    if q:
        qs = qs.filter(Q(cliente__nombre__icontains=q))
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    total_cobrado = qs.aggregate(total=Sum('monto'))['total'] or 0
    return render(request, 'pagos/lista.html', {'page_obj': page, 'q': q, 'total_cobrado': total_cobrado})


@login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registrado_por = request.user
            pago.save()
            messages.success(request, f'Pago de ${pago.monto:,.0f} registrado correctamente.')
            return redirect('detalle_pedido', pk=pago.pedido.pk)
    else:
        form = PagoForm()
        pedido_id = request.GET.get('pedido')
        if pedido_id:
            form.initial['pedido'] = pedido_id
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form.initial['cliente'] = pedido.cliente
    return render(request, 'pagos/form.html', {'form': form, 'titulo': 'Registrar Pago'})


@login_required
def deudas(request):
    """Vista de clientes con deuda pendiente."""
    clientes_deudores = []
    for cliente in Cliente.objects.filter(activo=True):
        deuda = cliente.saldo_deuda
        if deuda > 0:
            clientes_deudores.append({
                'cliente': cliente,
                'deuda': deuda,
                'pedidos_pendientes': cliente.pedidos.exclude(estado__in=['terminado','cancelado']).count()
            })
    clientes_deudores.sort(key=lambda x: x['deuda'], reverse=True)
    return render(request, 'pagos/deudas.html', {'clientes_deudores': clientes_deudores})
