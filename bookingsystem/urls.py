from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, VehicleViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls
