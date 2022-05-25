from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    founded = models.IntegerField()
    logo = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    player_id = models.IntegerField()
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    position = models.CharField(max_length=50)
    photo = models.CharField(max_length=250)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        ordering = ('team__name', 'position','name')

    def __str__(self):
        return f'{self.team} - {self.name}'