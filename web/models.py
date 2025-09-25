from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Plataforma(models.Model):
    nombre = models.CharField(max_length=50)
    dias_arriendo = models.IntegerField()
    precio_dias_atraso = models.IntegerField()

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    anio = models.IntegerField()
    fecha = models.DateField(null=True, blank=True) 
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    arrendador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    disponible = models.BooleanField(default=True) #para indicar que el juego esta disponible 

    def __str__(self):
        return self.titulo


class Arriendo(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_arriendo = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='arriendos', on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, related_name='arriendos', on_delete=models.CASCADE)

    def __str__(self):
        id = self.id
        fecha_arriendo = self.fecha_arriendo
        usuario = self.user.username 
        juego = self.juego.titulo
        plataforma = self.juego.plataforma.nombre
        return f'{id} | User: {usuario} | Juego: {juego} | Plataforma: {plataforma} | Fecha Arriendo: {fecha_arriendo}'
        
    
    class Meta:
        permissions = [
            ("agregar_juegos", "agregar nuevos juegos"),
        ]
