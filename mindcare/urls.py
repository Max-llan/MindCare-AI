from django.contrib import admin
from django.urls import path
from api.views import (
    LoginView,
    RegistroView,
    home,
    analizar_form,
    EvaluacionEmocionalView,
    AnalizarTextoView,
    login_page,
    registro_page,
    chatbot_page,
    ChatbotView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", login_page, name="login-page"),
    path("registro/", registro_page, name="registro-page"),
    path("chatbot/", chatbot_page, name="chatbot-page"),

    # AUTH
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/registro/', RegistroView.as_view(), name="registro"),

    # FRONTEND / PÁGINAS
    path('', home, name='home'),
    path("analizar/", analizar_form, name="analizar"),

    # API
    path('api/evaluaciones/', EvaluacionEmocionalView.as_view(), name="evaluaciones"),
    path('api/analizar-texto/', AnalizarTextoView.as_view(), name="analizar-texto"),
    path('api/chatbot/', ChatbotView.as_view(), name="chatbot"),
]
