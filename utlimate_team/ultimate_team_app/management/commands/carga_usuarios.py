from datetime import datetime

from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import random


class Command(BaseCommand):
    """Creación inicial de 30 usuarios"""

    def handle(self, *args, **options):
        fake = Faker('es_ES')
        rol_asignado= Rol.objects.get(nombre="usuario")
        for i in range(30):

            usuario = Usuario(
                nombre=fake.first_name(),
                nick=fake.user_name(),
                correo=fake.email(),
                password=fake.password(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
                fecha_registro=datetime.now().date(),
                equipo=False

            )
            usuario.save()
            usuario.rol.add(rol_asignado)