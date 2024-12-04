from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, VehicleViewSet, BookingViewSet, DepartementViewSet

router = DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('vehicles', VehicleViewSet)
router.register('bookings', BookingViewSet)
router.register('departements', DepartementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]