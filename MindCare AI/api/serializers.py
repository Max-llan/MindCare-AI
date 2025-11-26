from rest_framework import serializers
from .models import Usuario, EvaluacionEmocional

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class EvaluacionEmocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionEmocional
        fields = '__all__'
