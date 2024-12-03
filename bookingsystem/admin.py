from django.contrib import admin
from .models import Room, Vehicle, Booking, Driver
from django.core.exceptions import ValidationError


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'status')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'status')
    list_filter = ('type', 'status')
    search_fields = ('name', 'driver__name')  # Enable searching by driver
    fields = ('name', 'type', 'capacity', 'status', 'driver')  # Tampilkan driver di form admin

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number')
    search_fields = ('name', 'license_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resource_type', 'requester_name', 'start_time', 'end_time', 'status')
    list_editable = ('status',)  # Admin dapat mengedit status langsung dari list view
    list_filter = ('status', 'resource_type')  # Tambahkan filter
    search_fields = ('requester_name',)  # Kolom pencarian

    # Tampilkan field yang relevan berdasarkan resource_type
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.resource_type == 'Room':
            fields.remove('vehicle')  # Sembunyikan vehicle jika Room
        elif obj and obj.resource_type == 'Vehicle':
            fields.remove('room')  # Sembunyikan room jika Vehicle
        return fields

    # Validasi custom di admin sebelum menyimpan data
    def save_model(self, request, obj, form, change):
        try:
            obj.clean()  # Memastikan validasi di model dijalankan
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)  # Menampilkan error di form admin
