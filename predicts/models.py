from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class MatchPrediction(models.Model):
    match_id = models.IntegerField()
    homeTeamScore = models.PositiveIntegerField()
    awayTeamScore = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalScorer_id = models.IntegerField()
    checked = models.BooleanField(default=False)
    points = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'MD:{self.pk}- ID: {self.match_id}-{self.user}- {self.homeTeamScore} : {self.awayTeamScore}'

    # @property
    # def is_past_due(self):
    #     return timezone.now() > self.match.date


# class League(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, unique=True)
#     pin = models.IntegerField(max_length=6)
#     admin = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='league_admin')
#     users = models.ManyToManyField(User, related_name='league_users')
#     create_date = models.DateTimeField(auto_now_add=True)
#     rules = models.TextField(max_length=500, blank=True)
    

#     def __str__(self):
#         return self.name