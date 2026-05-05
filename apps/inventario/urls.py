from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet

router = DefaultRouter()
router.register('', MaterialViewSet, basename='inventario')
urlpatterns = router.urls
