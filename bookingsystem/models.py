from django.db import models
from django.core.exceptions import ValidationError

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    status = models.CharField(max_length=50, choices=[
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
    ])

    def __str__(self):
        return self.name

    def is_available(self, start_time, end_time):
        # Periksa jika Room ini sudah dipesan pada rentang waktu tertentu
        return not Booking.objects.filter(
            resource_type='Room',
            room=self,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Van', 'Van'),
        ('Truck', 'Truck'),
    ])
    capacity = models.IntegerField()
    status = models.CharField(max_length=50, choices=[
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
    ])

    def __str__(self):
        return self.name

    def is_available(self, start_time, end_time):
        # Periksa jika Vehicle ini sudah dipesan pada rentang waktu tertentu
        return not Booking.objects.filter(
            resource_type='Vehicle',
            vehicle=self,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

class Booking(models.Model):
    resource_type = models.CharField(
        max_length=50,
        choices=[('Room', 'Room'), ('Vehicle', 'Vehicle')]
    )
    room = models.ForeignKey(
        'Room', on_delete=models.SET_NULL, null=True, blank=True
    )
    vehicle = models.ForeignKey(
        'Vehicle', on_delete=models.SET_NULL, null=True, blank=True
    )
    destination_address = models.CharField(max_length=255, null=True)
    travel_description = models.TextField(null=True)
    requester_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
    max_length=50,
    choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
    default='Pending'
    )


    def clean(self):
        # Jalankan validasi hanya jika status adalah Pending
        if self.status == 'Pending':
            # Validasi untuk resource_type 'Room'
            if self.resource_type == 'Room':
                if not self.room:
                    raise ValidationError("Room is required when resource_type is 'Room'.")
                if not self.room.is_available(self.start_time, self.end_time):
                    raise ValidationError(f"{self.room.name} is already booked for the selected time.")

            # Validasi untuk resource_type 'Vehicle'
            elif self.resource_type == 'Vehicle':
                if not self.vehicle:
                    raise ValidationError("Vehicle is required when resource_type is 'Vehicle'.")
                if not self.vehicle.is_available(self.start_time, self.end_time):
                    raise ValidationError(f"{self.vehicle.name} is already booked for the selected time.")
                if not self.destination_address:
                    raise ValidationError("Destination address is required for Vehicle bookings.")
                if not self.travel_description:
                    raise ValidationError("Travel description is required for Vehicle bookings.")

        # Jika status bukan Pending, validasi tumpang tindih dilewati
        super().clean()

    def is_pending(self):
        return self.status == 'Pending'

    def __str__(self):
        if self.resource_type == 'Room' and self.room:
            return f"Room Booking: {self.room.name} by {self.requester_name}"
        elif self.resource_type == 'Vehicle' and self.vehicle:
            return f"Vehicle Booking: {self.vehicle.name} by {self.requester_name}"
        return f"{self.resource_type} Booking by {self.requester_name}"