from django.apps import AppConfig


class BookingsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookingsystem'

    def ready(self):
        from .utils.notification import FCMNotification
        FCMNotification.initialize()

        return super().ready()