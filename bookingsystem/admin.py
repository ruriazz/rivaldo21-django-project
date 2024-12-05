from django.contrib import admin
from django.shortcuts import render
from .models import Room, Vehicle, Booking, Driver, Departement
from django.core.exceptions import ValidationError


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'status')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)    


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'status', 'driver')
    list_filter = ('type', 'status')
    search_fields = ('name', 'driver__name')
    fields = ('name', 'type', 'capacity', 'status', 'driver')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number')
    search_fields = ('name', 'license_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'requester_name', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'resource_type']
    search_fields = ['requester_name']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:  
            if obj.resource_type == 'Room':
                fields.remove('destination_address')  
            elif obj.resource_type == 'Vehicle':
                fields.remove('room')  
        return fields

    def save_model(self, request, obj, form, change):
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['required_fields'] = ['departement', 'destination_address', 'room', 'vehicle']
        return super().changeform_view(request, object_id, form_url, extra_context)
