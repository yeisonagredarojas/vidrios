from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Material
from .forms import MaterialForm


@login_required
def lista_inventario(request):
    q = request.GET.get('q', '')
    stock_filter = request.GET.get('stock', '')
    qs = Material.objects.filter(activo=True).select_related('proveedor')
    if q:
        qs = qs.filter(Q(tipo_material__icontains=q))
    bajo_stock_count = sum(1 for m in Material.objects.filter(activo=True) if m.bajo_stock)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/lista.html', {
        'page_obj': page, 'q': q, 'bajo_stock_count': bajo_stock_count
    })


@login_required
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material agregado al inventario.')
            return redirect('lista_inventario')
    else:
        form = MaterialForm()
    return render(request, 'inventario/form.html', {'form': form, 'titulo': 'Nuevo Material'})


@login_required
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material actualizado.')
            return redirect('lista_inventario')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'inventario/form.html', {'form': form, 'titulo': 'Editar Material', 'material': material})
