"""
Vistas principales: dashboard, landing page, redirecciones.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido
from apps.pagos.models import Pago
from apps.inventario.models import Material
from apps.cotizaciones.models import ConfiguracionPrecios


def home_redirect(request):
    """Redirige al dashboard si autenticado, sino al login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('landing')


@login_required
def dashboard(request):
    """Panel de control principal con estadísticas clave del negocio."""
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)

    # === Estadísticas principales ===
    total_clientes = Cliente.objects.count()
    clientes_nuevos = Cliente.objects.filter(fecha_registro__gte=hace_30_dias).count()

    # Pedidos
    pedidos_qs = Pedido.objects.all()
    total_pedidos = pedidos_qs.count()
    pedidos_pendientes = pedidos_qs.filter(estado__in=['cotizado', 'abonado', 'en_proceso']).count()
    pedidos_mes = pedidos_qs.filter(fecha__gte=hace_30_dias).count()

    # Finanzas
    ingresos_mes = Pago.objects.filter(
        fecha_pago__gte=hace_30_dias
    ).aggregate(total=Sum('monto'))['total'] or 0

    # Deudas pendientes (precio_total - pagado)
    clientes_con_deuda = Cliente.objects.filter(
        pedidos__estado__in=['abonado', 'en_proceso', 'terminado']
    ).annotate(
        deuda=Sum('pedidos__precio_total') - Sum('pedidos__pagos__monto')
    ).filter(deuda__gt=0)
    total_deudas = clientes_con_deuda.aggregate(
        total=Sum('deuda')
    )['total'] or 0

    # Inventario bajo stock
    materiales_bajo_stock = Material.objects.filter(
        cantidad__lte=models_stock_minimo()
    ).count()

    # Pedidos por estado para gráfica
    estados_pedidos = list(
        pedidos_qs.values('estado').annotate(total=Count('id'))
    )

    # Últimos pedidos
    ultimos_pedidos = Pedido.objects.select_related('cliente').order_by('-fecha')[:8]

    # Ventas últimos 7 días (para gráfica de línea)
    ventas_semana = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        monto = Pago.objects.filter(fecha_pago=dia).aggregate(
            total=Sum('monto')
        )['total'] or 0
        ventas_semana.append({
            'dia': dia.strftime('%d/%m'),
            'monto': float(monto)
        })

    context = {
        'total_clientes': total_clientes,
        'clientes_nuevos': clientes_nuevos,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_mes': pedidos_mes,
        'ingresos_mes': ingresos_mes,
        'total_deudas': total_deudas,
        'materiales_bajo_stock': materiales_bajo_stock,
        'estados_pedidos': estados_pedidos,
        'ultimos_pedidos': ultimos_pedidos,
        'ventas_semana': ventas_semana,
    }
    return render(request, 'dashboard.html', context)


def models_stock_minimo():
    """Helper: retorna referencia al campo stock_minimo para comparación."""
    from django.db.models import F
    return F('stock_minimo')


def landing_page(request):
    """Página pública de la empresa con catálogo y formulario de contacto."""
    return render(request, 'public/landing.html')


def solicitar_cotizacion_publica(request):
    """Formulario público para solicitar cotización (envía por WhatsApp/email)."""
    from apps.cotizaciones.services import calcular_precio
    from apps.cotizaciones.models import ConfiguracionPrecios

    if request.method == 'POST':
        datos = {
            'nombre': request.POST.get('nombre'),
            'telefono': request.POST.get('telefono'),
            'correo': request.POST.get('correo'),
            'tipo_vidrio': request.POST.get('tipo_vidrio'),
            'ancho': float(request.POST.get('ancho', 0)),
            'alto': float(request.POST.get('alto', 0)),
            'tipo_trabajo': request.POST.get('tipo_trabajo'),
            'ciudad_entrega': request.POST.get('ciudad_entrega', ''),
            'es_envio_nacional': request.POST.get('es_envio_nacional') == 'on',
        }

        try:
            config_precios = ConfiguracionPrecios.objects.first()
            resultado = calcular_precio(datos, config_precios)

            # Enviar notificación WhatsApp mock
            from apps.pedidos.services import enviar_whatsapp_notificacion
            mensaje = (
                f"🏭 Nueva solicitud de cotización pública:\n"
                f"Cliente: {datos['nombre']}\n"
                f"Teléfono: {datos['telefono']}\n"
                f"Vidrio: {datos['tipo_vidrio']} {datos['ancho']}m x {datos['alto']}m\n"
                f"Precio estimado: ${resultado['precio_total']:,.0f}"
            )
            enviar_whatsapp_notificacion(datos['telefono'], mensaje)

            return JsonResponse({
                'success': True,
                'precio_total': resultado['precio_total'],
                'area': resultado['area'],
                'desglose': resultado['desglose'],
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return render(request, 'public/cotizacion_form.html')
