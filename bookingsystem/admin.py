from django.contrib import admin
from .models import Room, Vehicle, Booking
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
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resource_type', 'requester_name', 'start_time', 'end_time', 'status')
    list_editable = ('status',)  # Admin dapat mengedit status langsung dari list view
    list_filter = ('status', 'resource_type')  # Tambahkan filter
    search_fields = ('requester_name',)  # Kolom pencarian
    exclude = ('room', 'vehicle')  # Kolom ini dikelola otomatis


    # Validasi custom di admin sebelum menyimpan data
    def save_model(self, request, obj, form, change):
        try:
            obj.clean()  # Memastikan validasi di model dijalankan
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)  # Menampilkan error di form admin
