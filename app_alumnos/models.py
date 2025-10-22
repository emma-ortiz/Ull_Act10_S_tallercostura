from django.db import models

# Create your models here.
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"