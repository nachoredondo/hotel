from django.db import models
from sqlalchemy import true

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=10, verbose_name="Nombre")
    capacity = models.IntegerField(verbose_name="Capacidad")
    price = models.IntegerField(verbose_name="Precio")


class Reservation(models.Model):
    entry_date = models.DateField(verbose_name="Fecha de entrada")
    departure_date = models.DateField(verbose_name="Fecha de salida")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Habitación")
    n_guests = models.IntegerField(verbose_name="Invitados")
    name = models.CharField(max_length=20)
    mail = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=11, verbose_name="Teléfono")
    price = models.IntegerField(verbose_name="Precio")
    localizator = models.CharField(max_length=20, verbose_name="Localizador")