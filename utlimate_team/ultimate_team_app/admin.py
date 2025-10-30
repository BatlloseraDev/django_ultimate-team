from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(tabla) //nombre de modelo
admin.site.register(Jugador)
admin.site.register(Posicion)
admin.site.register(Equipo)
admin.site.register(Usuario)
admin.site.register(Rol)