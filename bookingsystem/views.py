from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CustomLoginSerializer
from rest_framework import viewsets, status
from .serializers import CustomLoginSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet  
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Purpose, Room, Vehicle, Booking, Departement
from .serializers import (
    PurposeSerializer,
    RoomSerializer,
    VehicleSerializer,
    BookingSerializer,
    DepartementSerializer,
)

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        })

class PurposeViewSet(ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = PurposeSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('room', 'vehicle', 'departement').all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]  
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(requester_name=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if not start_time or not end_time:
            return Response(
                {"error": "start_time and end_time are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            return Response(
                {"error": "start_time and end_time must be in ISO-8601 format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if start_time >= end_time:
            return Response(
                {"error": "start_time must be earlier than end_time."},
                status=status.HTTP_400_BAD_REQUEST
            )
        available_rooms = Room.objects.exclude(
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time,
            booking__status='Approved'
        )
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def available(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if not start_time or not end_time:
            return Response(
                {"error": "start_time and end_time are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            return Response(
                {"error": "start_time and end_time must be in ISO-8601 format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if start_time >= end_time:
            return Response(
                {"error": "start_time must be earlier than end_time."},
                status=status.HTTP_400_BAD_REQUEST
            )
        available_vehicles = Vehicle.objects.exclude(
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time,
            booking__status='Approved'
        )
        serializer = self.get_serializer(available_vehicles, many=True)
        return Response(serializer.data)

class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

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
