from django.contrib import admin
from .models import Juego, Plataforma, Genero, Arriendo

admin.site.register(Juego)
admin.site.register(Genero)
admin.site.register(Plataforma)
admin.site.register(Arriendo)
