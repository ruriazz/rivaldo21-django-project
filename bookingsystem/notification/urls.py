from django.urls import path
from .views import NotificationApiView, OpenNotificationApiView

urlpatterns = [
    path("", NotificationApiView.as_view({"get": "get_list"})),
    path("read", NotificationApiView.as_view({"post": "read_all"})),
    path(
        "token",
        NotificationApiView.as_view({"post": "store_fcm_token"}),
    ),
    path(
        "token/delete",
        OpenNotificationApiView.as_view({"delete": "delete_fcm_token"}),
    ),
]
