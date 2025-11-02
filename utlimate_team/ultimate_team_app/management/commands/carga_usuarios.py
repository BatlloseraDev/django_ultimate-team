from datetime import datetime

from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import random


class Command(BaseCommand):
    """Creación inicial de 30 usuarios (3 de ellos administradores)"""

    def handle(self, *args, **options):
        fake = Faker('es_ES')

        # Creación de roles
        rol_administrador = Rol(nombre="administrador")
        rol_administrador.save()

        rol_usuario = Rol(nombre="usuario")
        rol_usuario.save()

        for i in range(30):
            # Los tres primeros usuarios serán administradores
            rol_asignado = rol_administrador if i < 3 else rol_usuario

            usuario = Usuario(
                nombre=fake.first_name(),
                nick=fake.user_name(),
                correo=fake.email(),
                password=fake.password(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
                fecha_registro=datetime.now().date(),
                equipo=False,
                rol=rol_asignado
            )
            usuario.save()
