import jwt
from datetime import datetime, timedelta
from django.conf import settings


def crear_token_acceso(usuario_id):
    payload = {
        "user_id": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verificar_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
