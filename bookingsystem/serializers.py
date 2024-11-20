from rest_framework import serializers
from .models import Room, Vehicle, Booking

# Serializer untuk Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

# Serializer untuk Vehicle
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

# Serializer untuk Booking
class BookingSerializer(serializers.ModelSerializer):
    # Menambahkan detail Room dan Vehicle
    room_details = RoomSerializer(source='room', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'resource_type', 'room', 'vehicle', 
            'room_details', 'vehicle_details',
            'requester_name', 'start_time', 'end_time', 
            'destination_address', 'travel_description', 'status'
        ]
        read_only_fields = ['status']  # User tidak bisa mengubah status langsung

    def validate(self, data):
        # Validasi bahwa Room atau Vehicle dipilih sesuai dengan resource_type
        if data['resource_type'] == 'Room' and not data.get('room'):
            raise serializers.ValidationError("You must select a Room for this booking.")
        if data['resource_type'] == 'Vehicle' and not data.get('vehicle'):
            raise serializers.ValidationError("You must select a Vehicle for this booking.")
        if data['resource_type'] == 'Vehicle' and (
            not data.get('destination_address') or not data.get('travel_description')
        ):
            raise serializers.ValidationError(
                "Destination address and travel description are required for Vehicle bookings."
            )

        # Validasi booking tumpang tindih
        overlapping_bookings = Booking.objects.filter(
            resource_type=data['resource_type'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
        )
        if data['resource_type'] == 'Room':
            overlapping_bookings = overlapping_bookings.filter(room=data['room'])
        elif data['resource_type'] == 'Vehicle':
            overlapping_bookings = overlapping_bookings.filter(vehicle=data['vehicle'])

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                f"The selected {data['resource_type']} is already booked for the given time."
            )

        return data

    def create(self, validated_data):
        # Atur status default menjadi Pending
        validated_data['status'] = 'Pending'
        return super().create(validated_data)
