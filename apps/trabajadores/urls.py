from rest_framework.routers import DefaultRouter
from .views import TrabajadorViewSet
router = DefaultRouter()
router.register('', TrabajadorViewSet, basename='trabajadores')
urlpatterns = router.urls
