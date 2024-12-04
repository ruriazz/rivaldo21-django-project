from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q


class Departement(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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

    def is_in_use(self, start_time, end_time):
        # Periksa jika Room sedang digunakan pada waktu tertentu
        return Booking.objects.filter(
            resource_type='Room',
            room=self,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='Approved'
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
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )

    def __str__(self):
        return f"{self.name} ({self.driver.name if self.driver else 'No Driver'})"

    def is_in_use(self, start_time, end_time):
        # Periksa jika Vehicle sedang digunakan pada waktu tertentu
        return Booking.objects.filter(
            resource_type='Vehicle',
            vehicle=self,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='Approved'
        ).exists()


class Booking(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('Room', 'Room'),
        ('Vehicle', 'Vehicle'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(
        'Departement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    destination_address = models.CharField(max_length=255, null=False, blank=False)  # Harus diisi
    travel_description = models.TextField(null=False, blank=False)  # Harus diisi
    requester_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        if self.resource_type == 'Room' and self.room.is_in_use(self.start_time, self.end_time):
            raise ValidationError(f"Room {self.room.name} is already in use.")

        if self.resource_type == 'Vehicle' and self.vehicle.is_in_use(self.start_time, self.end_time):
            raise ValidationError(f"Vehicle {self.vehicle.name} is already in use.")

    def __str__(self):
        if self.resource_type == 'Room' and self.room:
            return f"Room Booking: {self.room.name} by {self.requester_name}"
        elif self.resource_type == 'Vehicle' and self.vehicle:
            return f"Vehicle Booking: {self.vehicle.name} by {self.requester_name}"
        return f"{self.resource_type} Booking by {self.requester_name}"


    def __str__(self):
        if self.resource_type == 'Room' and self.room:
            return f"Room Booking: {self.room.name} by {self.requester_name}"
        elif self.resource_type == 'Vehicle' and self.vehicle:
            return f"Vehicle Booking: {self.vehicle.name} by {self.requester_name}"
        return f"{self.resource_type} Booking by {self.requester_name}"
