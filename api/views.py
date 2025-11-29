from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from datetime import datetime, timedelta
import jwt

from .models import Usuario, EvaluacionEmocional
from .serializers import UsuarioSerializer, EvaluacionEmocionalSerializer
from .ia import analizar_texto
from .auth_decorators import requiere_token


# =============================
#   VISTA PRINCIPAL (HTML)
# =============================
def home(request):
    return render(request, "index.html")


# =============================
#   REGISTRO
# =============================
class RegistroView(APIView):
    permission_classes = []

    def post(self, request):
        nombre = request.data.get("nombre")
        correo = request.data.get("correo")
        contraseña = request.data.get("contraseña")

        if not nombre or not correo or not contraseña:
            return Response({"error": "Todos los campos son obligatorios"}, status=400)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({"error": "El correo ya está registrado"}, status=400)

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contraseña=make_password(contraseña)     # 🔥 Hash seguro
        )
        usuario.save()

        return Response({"mensaje": "Usuario registrado correctamente"}, status=201)


# =============================
#   LOGIN
# =============================
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        correo = request.data.get("correo")
        contraseña = request.data.get("contraseña")

        if not correo or not contraseña:
            return Response({"error": "correo y contraseña requeridos"}, status=400)

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "credenciales inválidas"}, status=401)

        if not check_password(contraseña, usuario.contraseña):
            return Response({"error": "credenciales inválidas"}, status=401)

        # Crear token manual
        payload = {
            "user_id": usuario.id,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"access": token})


# =============================
#   EVALUACIONES (PROTEGIDO)
# =============================
class EvaluacionEmocionalView(APIView):

    @requiere_token
    def get(self, request):
        evaluaciones = EvaluacionEmocional.objects.filter(usuario=request.usuario)
        serializer = EvaluacionEmocionalSerializer(evaluaciones, many=True)
        return Response(serializer.data)

    @requiere_token
    def post(self, request):
        texto = request.data.get("texto", "")

        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        data = {
            "usuario": request.usuario.id,
            "texto": texto,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion
        }

        serializer = EvaluacionEmocionalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =============================
#   ANALIZAR TEXTO (API)
# =============================
class AnalizarTextoView(APIView):

    @requiere_token
    def post(self, request):
        texto = request.data.get("texto", "")

        if texto == "":
            return Response({"error": "El campo 'texto' es obligatorio."}, status=400)

        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        return Response({
            "usuario": request.usuario.id,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion
        })


# =============================
#   HTML: FORMULARIO WEB
# =============================
def analizar_form(request):
    if request.method == "GET":
        return render(request, "analizar.html")

    if request.method == "POST":
        texto = request.POST.get("texto", "")

        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        contexto = {
            "texto_usuario": texto,
            "emocion": emocion,
            "nivel_estres": nivel_estres,
            "recomendacion": recomendacion
        }

        return render(request, "analizar.html", contexto)
