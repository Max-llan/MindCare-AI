from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Usuario, EvaluacionEmocional
from .auth_utils import crear_token_acceso

class EvaluacionEmocionalTests(TestCase):

    def setUp(self):
        # Crear usuario para autenticación
        self.usuario = Usuario.objects.create(nombre="TestUser", correo="test@example.com", contraseña="123456")
        self.token = crear_token_acceso(self.usuario.id)
        self.client = Client(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_crear_evaluacion_emocional(self):
        url = reverse('evaluaciones')
        data = {"texto": "Estoy muy estresado"}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('emocion', response.json())
    
    def test_get_evaluaciones_filtradas(self):
        # Crear evaluación manual
        EvaluacionEmocional.objects.create(usuario=self.usuario, texto="test", emocion="estres", nivel_estres=8, recomendacion="Respira")
        url = reverse('evaluaciones')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
