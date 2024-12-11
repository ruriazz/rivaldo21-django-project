from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  
from bookingsystem.views import RoomViewSet, VehicleViewSet, BookingViewSet, DepartementViewSet
from bookingsystem import views

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'departements', DepartementViewSet, basename='departements')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('api/login/', obtain_auth_token, name='api_login'),  
    path('', views.dashboard, name='dashboard'), 
]
