from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ConfiguracionPreciosViewSet, cotizar

router = DefaultRouter()
router.register('config', ConfiguracionPreciosViewSet, basename='config-precios')

urlpatterns = router.urls + [
    path('calcular/', cotizar, name='cotizar'),
]
