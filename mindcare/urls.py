from django.contrib import admin
from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('', home, name='home'),
    path('api/usuarios/', UsuarioView.as_view()),
    path("analizar", analizar_form, name="analizar"),
    path('api/evaluaciones/', EvaluacionEmocionalView.as_view()),
    path("api/analizar-texto/", AnalizarTextoView.as_view(), name="analizar-texto"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

