from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConfiguracionPrecios
from .forms import ConfiguracionPreciosForm

@login_required
def lista_configuracion(request):
    configs = ConfiguracionPrecios.objects.all()
    return render(request, 'cotizaciones/lista.html', {'configs': configs})

@login_required
def editar_configuracion(request, pk):
    config = get_object_or_404(ConfiguracionPrecios, pk=pk)
    if request.method == 'POST':
        form = ConfiguracionPreciosForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Precios actualizados correctamente.')
            return redirect('lista_configuracion')
    else:
        form = ConfiguracionPreciosForm(instance=config)
    return render(request, 'cotizaciones/form.html', {'form': form, 'config': config})
