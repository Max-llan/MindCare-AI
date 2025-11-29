from django.db import models
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.contraseña.startswith("pbkdf2_"):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

class EvaluacionEmocional(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='evaluaciones')
    texto = models.TextField()
    emocion = models.CharField(max_length=50)
    nivel_estres = models.IntegerField()
    recomendacion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.emocion}"
