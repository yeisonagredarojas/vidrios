from rest_framework import viewsets
from .models import Proveedor
from .serializers import ProveedorSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset         = Proveedor.objects.filter(activo=True)
    serializer_class = ProveedorSerializer
