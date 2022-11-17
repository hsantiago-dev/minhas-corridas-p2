from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Race(models.Model):
    name = models.CharField(max_length=100)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    registration_deadline = models.DateTimeField()
    start_date = models.DateTimeField()
    distance = models.IntegerField()
    start_hour = models.TimeField()
    registration_value = models.DecimalField(max_digits=5, decimal_places=2)
    registration_link = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    race = models.ForeignKey(Race, on_delete=models.RESTRICT)
    interaction = models.CharField(max_length=50)

    def __str__(self):
        return self.interaction


class RaceCommentary(models.Model):
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)
    date = models.DateTimeField()
    commentary = models.CharField(max_length=255)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.commentary
