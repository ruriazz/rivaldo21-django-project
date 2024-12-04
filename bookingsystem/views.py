from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from datetime import datetime
from .models import Room, Vehicle, Booking, Departement
from .serializers import RoomSerializer, VehicleSerializer, BookingSerializer, DepartementSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validasi format ISO-8601
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except (ValueError, TypeError):
            return Response(
                {"error": "start_time and end_time must be in ISO-8601 format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_time >= end_time:
            return Response(
                {"error": "start_time must be earlier than end_time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter rooms that are not booked in the given time range
        available_rooms = Room.objects.exclude(
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time,
            booking__status='Approved'
        )

        serializer = self.get_serializer(available_rooms, many=True, context={'request': request})
        return Response(serializer.data)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validasi format ISO-8601
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except (ValueError, TypeError):
            return Response(
                {"error": "start_time and end_time must be in ISO-8601 format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_time >= end_time:
            return Response(
                {"error": "start_time must be earlier than end_time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter vehicles that are not booked in the given time range
        available_vehicles = Vehicle.objects.exclude(
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time,
            booking__status='Approved'
        )

        serializer = self.get_serializer(available_vehicles, many=True, context={'request': request})
        return Response(serializer.data)


class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('room', 'vehicle', 'departement').all()
    serializer_class = BookingSerializer


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