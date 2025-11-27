from django.contrib import admin
from django.urls import path
from api.views import UsuarioView, EvaluacionEmocionalView
from api.views import LoginView
from api.views import AnalizarTextoView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),        # nueva ruta
    path('api/usuarios/', UsuarioView.as_view()),
    path('api/evaluaciones/', EvaluacionEmocionalView.as_view()),
    path("api/analizar-texto/", AnalizarTextoView.as_view(), name="analizar-texto"),
]

