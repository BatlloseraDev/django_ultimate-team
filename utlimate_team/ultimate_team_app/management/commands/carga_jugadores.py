from django.core.management.base import BaseCommand
from faker import Faker
from ...models import *
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Este archivo se encarga de realizar la carga inicial de los 150 jugadores
        :param args:
        :param options:
        :return:
        """
        pass