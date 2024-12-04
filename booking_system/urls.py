from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookingsystem.views import RoomViewSet, VehicleViewSet, BookingViewSet, DepartementViewSet
from bookingsystem import views

# DefaultRouter untuk API
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'departements', DepartementViewSet, basename='departements')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Masukkan router API di sini
    path('', views.dashboard, name='dashboard'),  # Dashboard
]
