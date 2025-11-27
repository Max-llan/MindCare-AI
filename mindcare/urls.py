from django.contrib import admin
from django.urls import path
from api.views import UsuarioView, EvaluacionEmocionalView
from api.views import LoginView
from api.views import AnalizarTextoView
from api.views import home
from api.views import analizar_form


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('', home, name='home'),
    path('api/usuarios/', UsuarioView.as_view()),
    path("analizar", analizar_form, name="analizar"),
    path('api/evaluaciones/', EvaluacionEmocionalView.as_view()),
    path("api/analizar-texto/", AnalizarTextoView.as_view(), name="analizar-texto"),
]

