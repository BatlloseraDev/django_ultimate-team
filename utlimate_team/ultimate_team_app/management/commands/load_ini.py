from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Este archivo se encarga de hacer la carga inicial de los datos estáticos de la base de datos
        como por ejemplo: roles y paises.
        :param args:
        :param options:
        :return:
        """
        pass
