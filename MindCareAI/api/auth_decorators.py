import jwt
from django.http import JsonResponse
from django.conf import settings
from api.models import Usuario

def requiere_token(view_func):
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Token no proporcionado"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except Exception:
            return JsonResponse({"error": "Token inválido"}, status=401)

        if not user_id:
            return JsonResponse({"error": "Token sin user_id"}, status=401)

        try:
            request.usuario = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)

        return view_func(self, request, *args, **kwargs)

    return wrapper
