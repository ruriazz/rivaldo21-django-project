from django.shortcuts import render
from rest_framework import viewsets
from .models import Room, Vehicle, Booking
from .models import Room, Vehicle, Booking, Departement
from .serializers import RoomSerializer, VehicleSerializer, BookingSerializer, DepartementSerializer

# ViewSet ba Room
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# ViewSet ba Vehicle
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# ViewSet untuk Departement
class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer    

# ViewSet ba Booking
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Funsaun dashboard
def dashboard(request):
    rooms = Room.objects.all()
    vehicles = Vehicle.objects.all()
    bookings = Booking.objects.select_related('room', 'vehicle', 'departement').all()
    departements = Departement.objects.all()  
    context = {
        'rooms': rooms,
        'vehicles': vehicles,
        'bookings': bookings,
        'departements': departements,  
    }
    return render(request, 'dashboard.html', context)

