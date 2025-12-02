from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import re

from .models import Usuario, EvaluacionEmocional
from .serializers import UsuarioSerializer, EvaluacionEmocionalSerializer
from .ia import analizar_texto, obtener_analisis_completo
from .auth_decorators import requiere_token
from .observers import get_event_manager
from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def registro_page(request):
    return render(request, "registro.html")



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

    def validar_contraseña(self, contraseña):
        """
        Valida que la contraseña cumpla con los requisitos:
        - Entre 8 y 16 caracteres
        - Al menos una letra minúscula
        - Al menos un carácter especial
        """
        errores = []
        
        if len(contraseña) < 8 or len(contraseña) > 16:
            errores.append("La contraseña debe tener entre 8 y 16 caracteres")
        
        if not re.search(r'[a-z]', contraseña):
            errores.append("La contraseña debe contener al menos una letra minúscula")
        
        if not re.search(r'[!@#$%^&*]', contraseña):
            errores.append("La contraseña debe contener al menos un carácter especial (!@#$%^&*)")
        
        return errores

    def post(self, request):
        nombre = request.data.get("nombre")
        correo = request.data.get("correo")
        contraseña = request.data.get("contraseña")

        if not nombre or not correo or not contraseña:
            return Response({"error": "Todos los campos son obligatorios"}, status=400)

        # Validar contraseña
        errores_contraseña = self.validar_contraseña(contraseña)
        if errores_contraseña:
            return Response({"error": " | ".join(errores_contraseña)}, status=400)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({"error": "El correo ya está registrado"}, status=400)

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contraseña=make_password(contraseña)     # 🔥 Hash seguro
        )
        usuario.save()

        # 🔥 PATRÓN OBSERVER: Notificar registro de usuario
        event_manager = get_event_manager()
        event_manager.usuario_registrado({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "fecha_creacion": usuario.fecha_creacion.isoformat()
        })

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

        # 🔥 PATRÓN OBSERVER: Notificar login de usuario
        event_manager = get_event_manager()
        event_manager.usuario_login({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo
        })

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
            
            # 🔥 PATRÓN OBSERVER: Notificar evaluación completada
            event_manager = get_event_manager()
            event_manager.evaluacion_completada(
                usuario_id=request.usuario.id,
                usuario_data={
                    "id": request.usuario.id,
                    "nombre": request.usuario.nombre,
                    "correo": request.usuario.correo
                },
                emocion=emocion,
                nivel_estres=nivel_estres,
                recomendacion=recomendacion
            )
            
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =============================
#   ANALIZAR TEXTO (API)
# =============================
class AnalizarTextoView(APIView):

    
    def post(self, request):
        texto = request.data.get("texto", "")

        if texto == "":
            return Response({"error": "El campo 'texto' es obligatorio."}, status=400)

        emocion, nivel_estres, recomendacion = analizar_texto(texto)

        return Response({
            "usuario": request.user.id,
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


# =============================
#   CHATBOT EMOCIONAL
# =============================
def chatbot_page(request):
    return render(request, "chatbot.html")


class ChatbotView(APIView):
    """
    API para el chatbot emocional.
    Recibe mensajes del usuario y retorna análisis emocional + respuesta.
    """
    
    @requiere_token
    def post(self, request):
        mensaje = request.data.get("mensaje", "").strip()

        if not mensaje:
            return Response({
                "respuesta": "No recibí tu mensaje. Por favor intenta de nuevo.",
                "analisis": {
                    "emocion": "neutral",
                    "emoji": "⚪",
                    "confianza": 0,
                    "nivel_estres": 5
                }
            }, status=400)

        # Obtener análisis completo
        analisis_completo = obtener_analisis_completo(mensaje)

        # Generar respuesta empática del chatbot
        respuesta = self._generar_respuesta_empatica(
            mensaje,
            analisis_completo["emocion_principal"],
            analisis_completo["nivel_estres"],
            analisis_completo["recomendacion"]
        )

        # Guardar evaluación
        try:
            evaluacion = EvaluacionEmocional.objects.create(
                usuario=request.usuario,
                texto=mensaje,
                emocion=analisis_completo["emocion_principal"],
                nivel_estres=int(round(analisis_completo["nivel_estres"])),
                recomendacion=analisis_completo["recomendacion"]
            )
            
            # 🔥 PATRÓN OBSERVER: Notificar evaluación completada
            event_manager = get_event_manager()
            event_manager.evaluacion_completada(
                usuario_id=request.usuario.id,
                usuario_data={
                    "id": request.usuario.id,
                    "nombre": request.usuario.nombre,
                    "correo": request.usuario.correo
                },
                emocion=analisis_completo["emocion_principal"],
                nivel_estres=int(round(analisis_completo["nivel_estres"])),
                recomendacion=analisis_completo["recomendacion"]
            )
            
        except Exception as e:
            print(f"Error al guardar evaluación: {e}")
            
            # 🔥 PATRÓN OBSERVER: Notificar error
            event_manager = get_event_manager()
            event_manager.error_ocurrido(
                error_type="database_error",
                error_message=str(e),
                context={"usuario_id": request.usuario.id, "accion": "guardar_evaluacion"}
            )

        return Response({
            "respuesta": respuesta,
            "analisis": {
                "emocion": analisis_completo["emocion_principal"],
                "emoji": analisis_completo["emojis"],
                "confianza": int(analisis_completo["confianza"]),
                "nivel_estres": int(round(analisis_completo["nivel_estres"]))
            }
        }, status=200)

    def _generar_respuesta_empatica(self, mensaje, emocion, nivel_estres, recomendacion):
        """Genera una respuesta empática basada en la emoción detectada con sesiones de apoyo."""
        
        respuestas_iniciales = {
            "alegría": "¡Me alegra mucho escuchar eso! 😊 Tu energía positiva es contagiosa.",
            "tristeza": "Entiendo que estés pasando por un momento difícil. 💙 Aquí estoy para escucharte.",
            "ansiedad": "Detecté algo de preocupación en tu mensaje. Respira profundo, esto es importante. 🧘",
            "enojo": "Parece que hay frustración. Está bien sentir esto. 💪 Hablemos al respecto.",
            "calma": "Noto que te sientes en paz. ¡Que bonito! Mantén esa armonía. ✨",
            "esperanza": "Veo optimismo en tus palabras. ¡Excelente! Confía en ti. 🎯",
            "soledad": "No estás solo/a. Muchas personas sienten lo mismo. Te estoy escuchando. 🤝",
            "culpa": "Es humano sentir culpa. Lo importante es aprender y crecer. 🌱",
            "confusión": "Veo que hay incertidumbre. No te preocupes, lo aclararemos juntos. 💭",
            "amor": "¡Qué hermoso sentir amor! 💕 Eso llena el corazón de significado.",
            "orgullo": "¡Estás muy orgulloso de ti! Eso es saludable. Mantén esa confianza. 👑",
            "vergüenza": "Entiendo tu vergüenza, pero no te define. Eres más que un momento. 💙",
            "miedo": "Es normal tener miedo. El valor es enfrentarlo a pesar del miedo. 💪",
            "gratitud": "¡Qué actitud tan hermosa! La gratitud transforma todo. 🙏",
            "frustración": "Tu frustración es válida. A veces necesitamos reconocerla antes de avanzar. 💫",
            "nostalgia": "Es bonito recordar. Aprecia esos momentos y crea nuevos. 📷",
            "admiración": "Tu admiración te inspira. Deja que te motive a crecer. ⭐",
            "disgusto": "Es válido alejarte de lo que te causa malestar. 🛡️",
            "sorpresa": "¡Qué inesperado! Los giros en la vida pueden traer oportunidades. 🎁",
            "vacío": "Ese vacío que sientes pide ser llenado de significado. Busquemos juntos. 🌟",
            "alivio": "¡Qué bien se siente aliviarse! Disfruta este descanso. 😌",
            "resentimiento": "El resentimiento pesa. El perdón puede liberarte. 🕊️",
            "compasión": "¡Qué corazón compasivo tienes! Extiende eso hacia ti también. 💚",
            "neutral": "Gracias por compartir conmigo. Aquí estoy para apoyarte. 👂"
        }

        respuesta_base = respuestas_iniciales.get(emocion, "Te entiendo perfectamente.")
        
        # Agregar recomendación personalizada
        respuesta_completa = f"{respuesta_base}\n\n📋 Mi recomendación: {recomendacion}"
        
        # SESIÓN DE APOYO según nivel de estrés
        if nivel_estres > 7:
            respuesta_completa += "\n\n⚠️ SESIÓN DE APOYO - ESTRÉS CRÍTICO"
            respuesta_completa += "\nTu nivel de estrés es muy alto. Aquí te ofrezco apoyo inmediato:"
            respuesta_completa += "\n\n🧘 Técnica de respiración 4-4-4:"
            respuesta_completa += "\n  1. Inhala profundamente por la nariz durante 4 segundos"
            respuesta_completa += "\n  2. Sostén la respiración durante 4 segundos"
            respuesta_completa += "\n  3. Exhala lentamente por la boca durante 4 segundos"
            respuesta_completa += "\n  4. Repite 5-10 veces"
            respuesta_completa += "\n\n💪 Acciones para ahora:"
            respuesta_completa += "\n  • Tómate 5 minutos de pausa"
            respuesta_completa += "\n  • Camina o muévete suavemente"
            respuesta_completa += "\n  • Bebe agua"
            respuesta_completa += "\n\n⚠️ Recursos de urgencia:"
            respuesta_completa += "\n  Si la situación empeora, busca ayuda profesional de inmediato"
            respuesta_completa += "\n  Línea de crisis: Disponible 24/7"
            
        elif nivel_estres > 5:
            respuesta_completa += "\n\n⚡ SESIÓN DE APOYO - ESTRÉS MODERADO"
            respuesta_completa += "\nTu nivel de estrés es moderado. Aquí hay acciones que pueden ayudarte:"
            respuesta_completa += "\n\n🧘 Técnicas de relajación:"
            respuesta_completa += "\n  • Meditación guiada (10 minutos)"
            respuesta_completa += "\n  • Ejercicio físico ligero (yoga, caminata)"
            respuesta_completa += "\n  • Música relajante o sonidos de la naturaleza"
            respuesta_completa += "\n\n🤝 Apoyo social:"
            respuesta_completa += "\n  • Conecta con un amigo cercano"
            respuesta_completa += "\n  • Comparte tus sentimientos con alguien de confianza"
            respuesta_completa += "\n  • Considera hablar con un terapeuta"
            respuesta_completa += "\n\n📝 Estrategias de autocuidado:"
            respuesta_completa += "\n  • Crea una rutina diaria de autosanación"
            respuesta_completa += "\n  • Establece límites saludables"
            respuesta_completa += "\n  • Dedica tiempo a actividades que disfrutes"
            
        else:
            respuesta_completa += "\n\n✅ SESIÓN DE APOYO - BIENESTAR SOSTENIBLE"
            respuesta_completa += "\nTu nivel de estrés está bajo. Mantén este bienestar:"
            respuesta_completa += "\n\n🌟 Clave para mantener la paz:"
            respuesta_completa += "\n  • Continúa con las actividades que te hacen feliz"
            respuesta_completa += "\n  • Cultiva conexiones positivas"
            respuesta_completa += "\n  • Practica gratitud diariamente"
            respuesta_completa += "\n  • Cuida tu sueño y alimentación"
            respuesta_completa += "\n\n💡 Para prevenir crisis futuras:"
            respuesta_completa += "\n  • Identifica tus disparadores emocionales"
            respuesta_completa += "\n  • Construye una red de apoyo sólida"
            respuesta_completa += "\n  • Desarrolla habilidades de resiliencia"

        return respuesta_completa
