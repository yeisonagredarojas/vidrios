from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Inicializa el sistema con datos base'

    def handle(self, *args, **options):
        self.stdout.write('Inicializando ERP Vidrios...')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@vidrios.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Usuario admin creado: admin / admin123'))
        else:
            self.stdout.write('Usuario admin ya existe')

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
            self.stdout.write(self.style.SUCCESS('Precios configurados'))

        from apps.proveedores.models import Proveedor
        if not Proveedor.objects.exists():
            Proveedor.objects.create(
                nombre='Vidreria Central',
                contacto='Proveedor',
                telefono='3001234567',
                tipo_material='Vidrio',
            )

        from apps.inventario.models import Material
        if not Material.objects.exists():
            prov = Proveedor.objects.first()
            Material.objects.bulk_create([
                Material(tipo_material='Vidrio Normal 4mm', cantidad=50, unidad='m2',
                         stock_minimo=10, proveedor=prov, precio_compra=18000),
                Material(tipo_material='Espejo 3mm', cantidad=30, unidad='m2',
                         stock_minimo=8, proveedor=prov, precio_compra=25000),
            ])
            self.stdout.write(self.style.SUCCESS('Inventario creado'))

        from apps.clientes.models import Cliente
        if not Cliente.objects.exists():
            Cliente.objects.create(
                nombre='Cliente Ejemplo',
                telefono='3009876543',
                ciudad='Bogota',
            )

        self.stdout.write(self.style.SUCCESS(
            'Sistema listo! Entra en http://localhost:8000/dashboard/'
        ))
