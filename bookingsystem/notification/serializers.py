from rest_framework import serializers

from bookingsystem.models import UserNotification

class NotificationTokenValidator(serializers.Serializer):
    token = serializers.CharField(required=True)

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ('id', 'payload', 'is_read', 'created_at')