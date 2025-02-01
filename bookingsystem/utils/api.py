from functools import wraps
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication


class ApiResponse(JsonResponse):
    def __init__(self, data=None, detail=None, status_code=200, **kwargs):
        response = {
            k: v
            for k, v in {
                "detail": detail,
                "data": data,
            }.items()
            if v is not None
        }
        super().__init__(response, status=status_code, **kwargs)


class CookieSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def validate_request(serializer_class, source="data"):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            serializer = serializer_class(data=getattr(request, source))
            if not serializer.is_valid():
                return ApiResponse(detail=serializer.errors, status_code=400)
            setattr(request, f"validated_{source}", serializer.validated_data)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
