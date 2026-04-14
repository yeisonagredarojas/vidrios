from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trabajador
from .forms import TrabajadorForm


@login_required
def lista_trabajadores(request):
    trabajadores = Trabajador.objects.filter(activo=True)
    return render(request, 'trabajadores/lista.html', {'trabajadores': trabajadores})


@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trabajador registrado.')
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm()
    return render(request, 'trabajadores/form.html', {'form': form})


@login_required
def editar_trabajador(request, pk):
    t = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trabajador actualizado.')
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm(instance=t)
    return render(request, 'trabajadores/form.html', {'form': form, 'trabajador': t})
