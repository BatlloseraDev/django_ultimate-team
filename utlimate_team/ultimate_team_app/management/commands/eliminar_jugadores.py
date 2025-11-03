from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Este archivo se encarga de realizar la limpieza de los jugadores
        :param args:
        :param options:
        :return:
        """
        self.stdout.write(self.style.SUCCESS('INICIAMOS LA DESTRUCCION DE LOS DATOS'))
        if Jugador.objects.exists():
            Jugador.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('FIN DE LA DESTRUCCION DE LOS DATOS'))
        else:
            self.stdout.write(self.style.WARNING(f'No tiene datos'))