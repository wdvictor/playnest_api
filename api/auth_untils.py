# auth_utils.py
from django.http import JsonResponse
from django.conf import settings


def require_api_token(view_func):
    def wrapped_view(request, *args, **kwargs):
        token = request.headers.get("X-API-KEY")
        if token != settings.API_TOKEN:
            return JsonResponse({"detail": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view
