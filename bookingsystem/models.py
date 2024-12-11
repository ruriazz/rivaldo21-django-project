from django.db import models
from django.core.exceptions import ValidationError


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
        return self.bookings.filter(
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
        return self.bookings.filter(
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
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    departement = models.ForeignKey(
        Departement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    destination_address = models.CharField(max_length=255, null=True, blank=True)
    travel_description = models.TextField(null=False, blank=False)
    requester_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def clean(self):
        errors = {}
        # Validasi waktu mulai dan selesai
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                errors['start_time'] = "Start time must be before end time."
        else:
            errors['start_time'] = "Both start_time and end_time must be provided."

        # Validasi resource_type untuk Room
        if self.resource_type == 'Room':
            if not self.room:
                errors['room'] = "Room must be selected for Room booking."
            elif self.start_time and self.end_time and self.room.is_in_use(self.start_time, self.end_time):
                errors['room'] = f"Room {self.room.name} is already in use for the given time."

            if self.destination_address:
                errors['destination_address'] = "Destination address should not be provided for Room bookings."

        elif self.resource_type == 'Vehicle':
            if not self.vehicle:
                errors['vehicle'] = "Vehicle must be selected for Vehicle booking."
            elif self.start_time and self.end_time and self.vehicle.is_in_use(self.start_time, self.end_time):
                errors['vehicle'] = f"Vehicle {self.vehicle.name} is already in use for the given time."

            if not self.destination_address:
                errors['destination_address'] = "Destination address is required for Vehicle bookings."

        if not self.departement:
            errors['departement'] = "Departement is required for all bookings."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        if self.resource_type == 'Room' and self.room:
            return f"Room Booking: {self.room.name} by {self.requester_name}"
        elif self.resource_type == 'Vehicle' and self.vehicle:
            return f"Vehicle Booking: {self.vehicle.name} by {self.requester_name}"
        return f"{self.resource_type} Booking by {self.requester_name}"
