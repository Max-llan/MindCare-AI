import jwt
from datetime import datetime, timedelta
from django.conf import settings

def crear_token_acceso(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=3),  # expira en 3 horas
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
