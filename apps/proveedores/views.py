from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proveedor
from .forms import ProveedorForm


@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})


@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {'form': form})


@login_required
def editar_proveedor(request, pk):
    p = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=p)
    return render(request, 'proveedores/form.html', {'form': form, 'proveedor': p})
