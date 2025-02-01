from django.db import transaction
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookingsystem.utils.api import (
    ApiResponse,
    validate_request,
    CookieSessionAuthentication,
)
from bookingsystem import models
from .serializers import NotificationTokenValidator, UserNotificationSerializer


class NotificationApiView(viewsets.ViewSet):
    authentication_classes = [CookieSessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_list(request):
        status = request.query_params.get("status") or "unred"
        notifications = models.UserNotification.objects.filter(user=request.user)
        if status in ["read", "unread"]:
            notifications = notifications.filter(is_read=status == "read")

        serialized = UserNotificationSerializer(
            notifications.order_by("-id"), many=True
        )
        return ApiResponse(data=serialized.data)

    @staticmethod
    def read_all(request):
        models.UserNotification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        return ApiResponse(detail="All notifications marked as read")

    @staticmethod
    @validate_request(NotificationTokenValidator)
    def store_fcm_token(request):
        with transaction.atomic():
            models.FCMToken.objects.filter(
                token=request.validated_data["token"]
            ).delete()
            models.FCMToken.objects.create(
                user=request.user, token=request.validated_data["token"]
            )
        return ApiResponse(detail="Token stored successfully")


class OpenNotificationApiView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    @validate_request(NotificationTokenValidator)
    def delete_fcm_token(request):
        models.FCMToken.objects.filter(token=request.validated_data["token"]).delete()
        return ApiResponse(detail="Token deleted successfully")
