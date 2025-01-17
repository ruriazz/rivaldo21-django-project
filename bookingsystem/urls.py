from django.urls import path, include
from .views import LoginAPIView
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, VehicleViewSet, BookingViewSet, DepartementViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('vehicles', VehicleViewSet)
router.register('bookings', BookingViewSet)
router.register('departements', DepartementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api_login'),
]