"""
Script de inicializacion de datos base.
Se ejecuta automaticamente al levantar el contenedor.
"""
import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from apps.cotizaciones.models import ConfiguracionPrecios
from apps.proveedores.models import Proveedor
from apps.inventario.models import Material
from apps.clientes.models import Cliente

# 1. Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vidrios.com', 'admin123')
    print('[OK] Usuario admin creado  ->  admin / admin123')
else:
    print('[--] Usuario admin ya existe')

# 2. Precios
if not ConfiguracionPrecios.objects.exists():
    ConfiguracionPrecios.objects.create(
        nombre='Principal',
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
    print('[OK] Configuracion de precios creada')
else:
    print('[--] Precios ya existen')

# 3. Proveedor de ejemplo
if not Proveedor.objects.exists():
    Proveedor.objects.create(
        nombre='Vidreria Central S.A.',
        contacto='Carlos Lopez',
        telefono='3001234567',
        ciudad='Pasto',
        tipo_material='Vidrio float y templado',
    )
    print('[OK] Proveedor de ejemplo creado')

# 4. Inventario de ejemplo
if not Material.objects.exists():
    prov = Proveedor.objects.first()
    Material.objects.bulk_create([
        Material(tipo_material='Vidrio Normal 4mm',    cantidad=50, unidad='m2',     stock_minimo=10, proveedor=prov, precio_compra=18000),
        Material(tipo_material='Espejo 3mm',           cantidad=30, unidad='m2',     stock_minimo=8,  proveedor=prov, precio_compra=25000),
        Material(tipo_material='Vidrio Templado 6mm',  cantidad=20, unidad='m2',     stock_minimo=5,  proveedor=prov, precio_compra=60000),
        Material(tipo_material='Silicona Transparente',cantidad=24, unidad='unidad', stock_minimo=6,               precio_compra=12000),
        Material(tipo_material='Perfil Aluminio',      cantidad=100,unidad='metros', stock_minimo=20,              precio_compra=8000),
    ])
    print('[OK] Inventario inicial creado (5 materiales)')

# 5. Cliente de ejemplo
if not Cliente.objects.exists():
    Cliente.objects.create(
        nombre='Maria Garcia (Ejemplo)',
        telefono='3009876543',
        ciudad='Tumaco',
        direccion='Calle 10 # 5-20',
    )
    print('[OK] Cliente de ejemplo creado')

print('')
print('============================================')
print('  API lista en http://localhost:8000')
print('  Admin:    http://localhost:8000/admin/')
print('  Usuario:  admin')
print('  Clave:    admin123')
print('============================================')
