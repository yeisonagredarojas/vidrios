from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Cliente
from .forms import ClienteForm


@login_required
def lista_clientes(request):
    q = request.GET.get('q', '')
    ciudad = request.GET.get('ciudad', '')
    estado = request.GET.get('estado', '')
    qs = Cliente.objects.filter(activo=True)
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(telefono__icontains=q) | Q(correo__icontains=q))
    if ciudad:
        qs = qs.filter(ciudad__icontains=ciudad)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    ciudades = Cliente.objects.values_list('ciudad', flat=True).distinct().order_by('ciudad')
    return render(request, 'clientes/lista.html', {
        'page_obj': page, 'q': q, 'ciudad': ciudad, 'ciudades': ciudades
    })


@login_required
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pedidos = cliente.pedidos.all().order_by('-fecha')[:10]
    pagos = cliente.pagos.all().order_by('-fecha_pago')[:10]
    return render(request, 'clientes/detalle.html', {
        'cliente': cliente, 'pedidos': pedidos, 'pagos': pagos
    })


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre} creado exitosamente.')
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('detalle_cliente', pk=pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente', 'cliente': cliente})


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.activo = False
        cliente.save()
        messages.success(request, f'Cliente {cliente.nombre} eliminado.')
        return redirect('lista_clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})
