from datetime import datetime
from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import os
import django
import pandas as pd
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Este archivo se encarga de hacer la carga inicial de los datos estáticos de la base de datos
        como por ejemplo: roles y paises.
        """
        fake = Faker('es_ES')

        # Creación de roles
        rol_administrador = Rol(nombre="administrador")
        rol_administrador.save()

        rol_usuario = Rol(nombre="usuario")
        rol_usuario.save()

        #Creación de un usuario con el rol administrador
        usuario = Usuario(
            nombre=fake.first_name(),
            nick=fake.user_name(),
            correo=fake.email(),
            password=fake.password(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
            fecha_registro=datetime.now().date(),
            equipo=False,
            rol=rol_administrador
        )
        usuario.save()

        #Creación de nacionalidades
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ultimate_team.settings")
        django.setup()

        # Lee el archivo
        archivo = os.path.join(settings.BASE_DIR, "datos", "paisesyterritorios.xls")
        df = pd.read_excel(archivo)

        # Guardar nacionalidades en la base de datos (Los países están en la columna 5)
        for nombre in df.iloc[:, 5]:
            if isinstance(nombre, str) and nombre.strip():
                Nacionalidad.objects.get_or_create(nombre=nombre.strip())

