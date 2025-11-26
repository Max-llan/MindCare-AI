from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, EvaluacionEmocional
from .serializers import UsuarioSerializer, EvaluacionEmocionalSerializer
from django.contrib.auth.hashers import check_password
from .ia import analizar_texto
from .auth_utils import crear_token_acceso
from .auth_decorators import requiere_token

class UsuarioView(APIView):

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvaluacionEmocionalView(APIView):

    def get(self, request):
        evaluaciones = EvaluacionEmocional.objects.all()
        serializer = EvaluacionEmocionalSerializer(evaluaciones, many=True)
        return Response(serializer.data)

    @requiere_token
    def post(self, request):
        # ahora request.usuario es el objeto Usuario autenticado
        texto = request.data.get("texto", "")
        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        data = {
            "usuario": request.usuario.id,  # usamos usuario del token
            "texto": texto,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion
        }

        serializer = EvaluacionEmocionalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    POST /api/login/
    Body: { "correo": "<email>", "contraseña": "<pass>" }
    Respuesta: { "access": "<token>" }
    """
    def post(self, request):
        correo = request.data.get("correo")
        contraseña = request.data.get("contraseña")

        if not correo or not contraseña:
            return Response({"error": "correo y contraseña requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar contraseña: intentamos check_password (por si fue hashed),
        # si falla comparamos en texto plano (por compatibilidad con tu estado actual).
        valid = False
        try:
            valid = check_password(contraseña, usuario.contraseña)
        except Exception:
            valid = False

        if not valid:
            # fallback: comparar en claro (solo si tu DB almacena claro)
            if contraseña != usuario.contraseña:
                return Response({"error": "credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        
        token = crear_token_acceso(usuario.id)
        return Response({"access": token})
    
class AnalizarTextoView(APIView):

    @requiere_token
    def post(self, request):
        texto = request.data.get("texto", "")

        if texto == "":
            return Response({"error": "El campo 'texto' es obligatorio."},
                            status=status.HTTP_400_BAD_REQUEST)

        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        return Response({
            "usuario": request.usuario.id,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion
        })
