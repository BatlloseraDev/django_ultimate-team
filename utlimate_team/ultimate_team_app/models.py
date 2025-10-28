from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Posicion(models.Model):
    """
    Modelo para representar las posiciones de los jugadores en un equipo.
    """

    class TipoPosicion(models.TextChoices):
        PORTERO = 'POR', 'Portero'
        DEFENSA = 'DEF', 'Defensa'
        CENTROCAMPISTA = 'CEN', 'Centrocampista'
        DELANTERO = 'DEL', 'Delantero'

    siglas = models.CharField(
        max_length=3,
        unique=True,
        help_text='Siglas de la posición ej:( POR ,DFC, LTI, ...)'
    )#no puede ser null, ni blank, al momento de crearlo siempre generar una pero que no se repita
    significado = models.CharField(
        max_length=140,
        help_text='Nombre completo de la posición ej: Defensa Central'
    )
    tipo = models.CharField(
        max_length=3,
        choices=TipoPosicion.choices,
        help_text='El tipo de posición en el campo'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción más detallada de la posición y sus funciones.'
    )

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"

    def __str__(self):
        return self.significado


class Jugador(models.Model):
    """
    Modelo para representar a los jugadores en un equipo.
    """
    nombre =  models.CharField(
        max_length=100,
        help_text='Nombre del jugador'
    )

    nacionalidad = models.CharField(
        max_length=100,
        help_text='Nacionalidad del jugador'
    )
    equipo = models.CharField(
        max_length=100,
        help_text='Equipo real del jugador'
    )
    posicion_id= models.ForeignKey(
        Posicion,
        on_delete=models.PROTECT
    )
    pac = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Velocidad del jugador'
    )
    sho = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Disparo del jugador'
    )
    pas = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Pase del jugador'
    )
    dri = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Regate del jugador'
    )
    def_ = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Defensa del jugador'
    )#es def_ porque entra en conflicto con la palabra reservada
    phy = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text='Físico del jugador'
    )

    def stats(self):
        return {
            'pac': self.pac,
            'sho': self.sho,
            'pas': self.pas,
            'dri': self.dri,
            'def': self.def_,
            'phy': self.phy
        }
    def calcular_valoracion(self):
        """
        Calcula la valoración del jugador en base a sus estadísticas y tipo de jugador
        :return:
        """
        estadisticas = self.stats()
        pesos_por_posicion = {
            'POR': {'pac':0.05, 'sho':0.05, 'pas':0.15, 'dri':0.05, 'def':0.50, 'phy':0.20},
            'DEF': {'pac':0.20, 'sho':0.05, 'pas':0.15, 'dri':0.05, 'def':0.40, 'phy':0.15},
            'CEN': {'pac':0.20, 'sho':0.10, 'pas':0.35, 'dri':0.15, 'def':0.10, 'phy':0.10},
            'DEL': {'pac':0.30, 'sho':0.40, 'pas':0.05, 'dri':0.15, 'def':0.05, 'phy':0.05}

        }

        pos = self.posicion_id.nombre.upper()
        pesos = pesos_por_posicion.get(pos)
        if not pesos:
            return round(sum(estadisticas.values()) / len(estadisticas))

        valoracion = sum(estadisticas[stat] * peso for stat, peso in pesos.items())
        return round(valoracion)

    estadistica_final = calcular_valoracion()
    
    def __str__(self):
        return f'{self.nombre} - {self.estadistica_final}'

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
