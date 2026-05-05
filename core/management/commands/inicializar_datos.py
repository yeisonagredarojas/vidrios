from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea datos iniciales para probar la API en Postman'

    def handle(self, *args, **options):
        # 1. Superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@vidrios.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ admin creado  (admin / admin123)'))

        # 2. Precios
        from apps.cotizaciones.models import ConfiguracionPrecios
        if not ConfiguracionPrecios.objects.exists():
            ConfiguracionPrecios.objects.create(
                nombre='Principal', activo=True,
                precio_vidrio_normal_m2=25000, precio_vidrio_tallado_m2=45000,
                precio_espejo_m2=35000, precio_vidrio_templado_m2=80000,
                precio_vidrio_laminado_m2=65000, recargo_instalacion=20,
                recargo_diseno=30, costo_transporte_local=15000,
                costo_transporte_nacional=80000, area_minima_m2=0.25)
            self.stdout.write(self.style.SUCCESS('✅ Precios configurados'))

        # 3. Proveedor
        from apps.proveedores.models import Proveedor
        if not Proveedor.objects.exists():
            Proveedor.objects.create(
                nombre='Vidriería Central S.A.', contacto='Juan',
                telefono='3001234567', tipo_material='Vidrio float')
            self.stdout.write(self.style.SUCCESS('✅ Proveedor creado'))

        # 4. Inventario
        from apps.inventario.models import Material
        if not Material.objects.exists():
            prov = Proveedor.objects.first()
            Material.objects.bulk_create([
                Material(tipo_material='Vidrio Normal 4mm', cantidad=50, unidad='m2',
                         stock_minimo=10, proveedor=prov, precio_compra=18000),
                Material(tipo_material='Espejo 3mm', cantidad=30, unidad='m2',
                         stock_minimo=8, proveedor=prov, precio_compra=25000),
                Material(tipo_material='Silicona Transparente', cantidad=24,
                         unidad='unidad', stock_minimo=6, precio_compra=12000),
            ])
            self.stdout.write(self.style.SUCCESS('✅ Inventario creado'))

        # 5. Trabajador
        from apps.trabajadores.models import Trabajador
        if not Trabajador.objects.exists():
            Trabajador.objects.create(
                nombre='Carlos Instalador', rol='instalador', telefono='3009999999')
            self.stdout.write(self.style.SUCCESS('✅ Trabajador creado'))

        # 6. Cliente
        from apps.clientes.models import Cliente
        if not Cliente.objects.exists():
            Cliente.objects.create(
                nombre='María García', telefono='3001111111',
                ciudad='Tumaco', correo='maria@ejemplo.com')
            self.stdout.write(self.style.SUCCESS('✅ Cliente de ejemplo creado'))

        self.stdout.write(self.style.SUCCESS(
            '\n🚀 API lista en http://localhost:8000\n'
            '   Obtén tu token: POST /api/auth/login/\n'
            '   { "username": "admin", "password": "admin123" }'
        ))
