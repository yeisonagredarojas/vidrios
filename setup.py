import django
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vidrios.com', 'admin123')
    print('OK: admin creado - clave: admin123')
else:
    print('INFO: admin ya existe')

from apps.cotizaciones.models import ConfiguracionPrecios
if not ConfiguracionPrecios.objects.exists():
    ConfiguracionPrecios.objects.create(
        nombre='Configuracion Principal',
        activo=True,
        precio_vidrio_normal_m2=25000,
        precio_vidrio_tallado_m2=45000,
        precio_espejo_m2=35000,
        precio_vidrio_templado_m2=80000,
        precio_vidrio_laminado_m2=65000,
        recargo_instalacion=20,
        recargo_diseno=30,
        costo_transporte_local=15000,
        costo_transporte_nacional=80000,
        area_minima_m2=0.25,
    )
    print('OK: precios configurados')

from apps.proveedores.models import Proveedor
if not Proveedor.objects.exists():
    Proveedor.objects.create(
        nombre='Vidreria Central S.A.',
        contacto='Proveedor Principal',
        telefono='3001234567',
        tipo_material='Vidrio float',
    )
    print('OK: proveedor creado')

from apps.inventario.models import Material
if not Material.objects.exists():
    prov = Proveedor.objects.first()
    Material.objects.bulk_create([
        Material(tipo_material='Vidrio Normal 4mm', cantidad=50, unidad='m2', stock_minimo=10, proveedor=prov, precio_compra=18000),
        Material(tipo_material='Espejo 3mm', cantidad=30, unidad='m2', stock_minimo=8, proveedor=prov, precio_compra=25000),
        Material(tipo_material='Silicona Transparente', cantidad=24, unidad='unidad', stock_minimo=6, precio_compra=12000),
    ])
    print('OK: inventario creado')

from apps.clientes.models import Cliente
if not Cliente.objects.exists():
    Cliente.objects.create(nombre='Cliente Ejemplo', telefono='3009876543', ciudad='Bogota')
    print('OK: cliente ejemplo creado')

print('')
print('====================================')
print('SISTEMA LISTO!')
print('URL:      http://localhost:80')
print('Usuario:  admin')
print('Clave:    admin123')
print('====================================')