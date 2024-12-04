from django.shortcuts import render  # Tambahkan ini
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Room, Vehicle, Booking, Departement
from .serializers import RoomSerializer, VehicleSerializer, BookingSerializer, DepartementSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not start_time or not end_time:
            return Response(
                {"error": "start_time and end_time are required parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter rooms that are not booked in the given time range
        available_rooms = Room.objects.exclude(
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time
        )

        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if start_time and end_time:
            available_vehicles = Vehicle.objects.exclude(
                booking__start_time__lt=end_time,  # Perbaikan di sini
                booking__end_time__gt=start_time,  # Perbaikan di sini
                booking__status='Approved'        # Perbaikan di sini
            )
            serializer = self.get_serializer(available_vehicles, many=True, context={'request': request})
            return Response(serializer.data)
        return Response({"error": "Provide start_time and end_time"}, status=400)


class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('room', 'vehicle', 'departement').all()
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

