from rest_framework import viewsets
from .models import Trabajador
from .serializers import TrabajadorSerializer

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset         = Trabajador.objects.filter(activo=True)
    serializer_class = TrabajadorSerializer
