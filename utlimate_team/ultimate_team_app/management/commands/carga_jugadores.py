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
        self.stdout.write(self.style.SUCCESS('INICIAMOS LA CARGA DE LOS DATOS'))

        fake = Faker('es_Es')

        if Jugador.objects.exists():
            self.stdout.write(self.style.WARNING(f'Tiene ya datos'))
        else:
            #Porteros
            for i in range(30):
                jugador = Jugador(
                    nombre = fake.name(),
                    nacionalidad = random.choice(Nacionalidad.objects.all()),
                    equipo = fake.name(),
                    posicion_id = Posicion.objects.get(tipo='POR'),
                    pac = random.randint(1, 99),
                    sho = random.randint(1, 99),
                    pas = random.randint(1, 99),
                    dri = random.randint(1, 99),
                    defe = random.randint(1, 99),
                    phy = random.randint(1, 99)
                )
                jugador.save()

            #Defensas
            for i in range(40):
                jugador = Jugador(
                    nombre=fake.name(),
                    nacionalidad=random.choice(Nacionalidad.objects.all()),
                    equipo=fake.name(),
                    posicion_id=Posicion.objects.get(tipo='DEF'),
                    pac=random.randint(1, 99),
                    sho=random.randint(1, 99),
                    pas=random.randint(1, 99),
                    dri=random.randint(1, 99),
                    defe=random.randint(1, 99),
                    phy=random.randint(1, 99)
                )
                jugador.save()
            #CentroCampistas
            for i in range(40):
                jugador = Jugador(
                    nombre=fake.name(),
                    nacionalidad=random.choice(Nacionalidad.objects.all()),
                    equipo=fake.name(),
                    posicion_id=Posicion.objects.get(tipo='CEN'),
                    pac=random.randint(1, 99),
                    sho=random.randint(1, 99),
                    pas=random.randint(1, 99),
                    dri=random.randint(1, 99),
                    defe=random.randint(1, 99),
                    phy=random.randint(1, 99)
                )
                jugador.save()
            #Delanteros
            for i in range(40):
                jugador = Jugador(
                    nombre=fake.name(),
                    nacionalidad=random.choice(Nacionalidad.objects.all()),
                    equipo=fake.name(),
                    posicion_id=Posicion.objects.get(tipo='DEL'),
                    pac=random.randint(1, 99),
                    sho=random.randint(1, 99),
                    pas=random.randint(1, 99),
                    dri=random.randint(1, 99),
                    defe=random.randint(1, 99),
                    phy=random.randint(1, 99)
                )
                jugador.save()
            self.stdout.write(self.style.SUCCESS('FIN DE LA CARGA DE LOS DATOS'))

