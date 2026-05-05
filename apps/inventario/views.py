from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Material
from .serializers import MaterialSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset         = Material.objects.filter(activo=True)
    serializer_class = MaterialSerializer

    @action(detail=False, methods=['get'], url_path='bajo-stock')
    def bajo_stock(self, request):
        """GET /api/inventario/bajo-stock/ — materiales con stock critico."""
        qs = [m for m in self.get_queryset() if m.bajo_stock]
        return Response(MaterialSerializer(qs, many=True).data)
