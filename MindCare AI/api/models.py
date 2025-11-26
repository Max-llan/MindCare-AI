from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class EvaluacionEmocional(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='evaluaciones')
    texto = models.TextField()
    emocion = models.CharField(max_length=50)
    nivel_estres = models.IntegerField()
    recomendacion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.emocion}"
