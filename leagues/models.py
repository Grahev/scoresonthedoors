from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING

# Create your models here.
class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    pin = models.IntegerField()
    admin = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='league_admin')
    users = models.ManyToManyField(User, related_name='leagues')
    create_date = models.DateTimeField(auto_now_add=True)
    rules = models.TextField(max_length=500, blank=True)
    

    def __str__(self):
        return self.name