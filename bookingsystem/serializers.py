from rest_framework import serializers
from datetime import datetime
from .models import Room, Vehicle, Booking, Departement


class RoomSerializer(serializers.ModelSerializer):
    in_use = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_in_use(self, obj):
        request = self.context.get('request')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        try:
            if start_time and end_time:
                start_time = datetime.fromisoformat(start_time)
                end_time = datetime.fromisoformat(end_time)
                return obj.is_in_use(start_time, end_time)
        except (ValueError, TypeError):
            return False
        return False


class VehicleSerializer(serializers.ModelSerializer):
    in_use = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = '__all__'

    def get_in_use(self, obj):
        request = self.context.get('request')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        try:
            if start_time and end_time:
                start_time = datetime.fromisoformat(start_time)
                end_time = datetime.fromisoformat(end_time)
                return obj.is_in_use(start_time, end_time)
        except (ValueError, TypeError):
            return False
        return False


class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    room_details = RoomSerializer(source='room', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    departement_details = DepartementSerializer(source='departement', read_only=True)
    formatted_start_time = serializers.SerializerMethodField()
    formatted_end_time = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id', 'resource_type', 'room', 'vehicle', 'departement',
            'room_details', 'vehicle_details', 'departement_details',
            'requester_name', 'start_time', 'end_time',
            'formatted_start_time', 'formatted_end_time',
            'destination_address', 'travel_description', 'status'
        ]
        read_only_fields = ['status']

    def get_formatted_start_time(self, obj):
        return obj.start_time.strftime('%d-%m-%Y %H:%M')

    def get_formatted_end_time(self, obj):
        return obj.end_time.strftime('%d-%m-%Y %H:%M')

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Validasi waktu
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("start_time must be earlier than end_time.")
        else:
            raise serializers.ValidationError("Both start_time and end_time must be provided.")

        # Validasi resource_type
        resource_type = data.get('resource_type')
        if resource_type == 'Room':
            if not data.get('room'):
                raise serializers.ValidationError("Room must be selected for Room bookings.")
            if data.get('vehicle'):
                raise serializers.ValidationError("Vehicle cannot be selected for Room bookings.")
        elif resource_type == 'Vehicle':
            if not data.get('vehicle'):
                raise serializers.ValidationError("Vehicle must be selected for Vehicle bookings.")
            if not data.get('destination_address'):
                raise serializers.ValidationError("Destination address is required for Vehicle bookings.")

        # Validasi konflik waktu
        overlapping_bookings = Booking.objects.filter(
            resource_type=resource_type,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='Approved'
        )
        if resource_type == 'Room':
            overlapping_bookings = overlapping_bookings.filter(room=data.get('room'))
        elif resource_type == 'Vehicle':
            overlapping_bookings = overlapping_bookings.filter(vehicle=data.get('vehicle'))

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                f"The selected {resource_type} is already booked for the given time range."
            )

        return data

    def create(self, validated_data):
        # Atur status default menjadi Pending
        validated_data['status'] = 'Pending'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update instance booking
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        # Kondisional untuk menampilkan data yang relevan
        representation = super().to_representation(instance)
        if instance.resource_type == 'Room':
            representation.pop('vehicle_details', None)
        elif instance.resource_type == 'Vehicle':
            representation.pop('room_details', None)
        return representation