from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.utils import timezone
from django.contrib.auth.models import User
from teams_and_players.models import Team, Player
import os
import requests

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
# Create your models here.


class Match(models.Model):

    matchday = models.CharField(max_length=50)
    hTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    aTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateTimeField()
    status = models.CharField(max_length=20)
    hTeamScore = models.IntegerField(blank=True, null=True)
    aTeamScore = models.IntegerField(blank=True, null=True)
    goalScorers = models.ManyToManyField(Player, related_name='goal_scorers',blank=True)
    match_id = models.IntegerField()
    league = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Match | {self.matchday} - {self.hTeam} : {self.aTeam} - {self.status}'

    @property
    def is_past_due(self):
        return timezone.now() > self.date

    @property
    def is_active(self):
        return timezone.now() < self.date

    @property
    def md(self):
        day = self.matchday.split('-')[-1]
        return day

    @property
    def first_goal(self):
        first = MatchEvents.objects.filter(match=self).filter(type='Goal').first()
        try:
            f = first.player.name
        except:
            f = ""
        return f


class MatchPrediction(models.Model):
    matchApiId = models.IntegerField(default=0)
    homeTeamScore = models.PositiveIntegerField()
    homeTeamName = models.CharField(max_length=55)
    awayTeamScore = models.PositiveIntegerField()
    awayTeamName = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalScorerId = models.IntegerField(default=0)
    goalScorerName = models.CharField(max_length=55)
    checked = models.BooleanField(default=False)
    points = models.IntegerField(blank=True, null=True)
    league = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    
    def __str__(self):
        return f'Match Prediction | {self.user} - {self.homeTeamName} {self.homeTeamScore} : {self.awayTeamScore} {self.awayTeamName}'

    @property
    def is_past_due(self):
        return timezone.now() > self.match_date

    @property
    def is_active(self):
        return timezone.now() < self.match_date

    def first_goal_scorer(self):
        pass

class MatchResult(models.Model):
    code = (
        ('1','Home Team Won'),
        ('X','Draw'),
        ('2','Away Team Won'),
    )
    match_id = models.IntegerField()
    homeTeamResult = models.IntegerField()
    awayTeamResult = models.IntegerField()
    resultCode = models.CharField(max_length=1, choices=code)
    firstGoalScorerId = models.IntegerField(null=True, blank=True)
    firstGoalScorerName = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Match result | id{self.match_id} - code {self.resultCode}'

    
    
    

class MatchEvents(models.Model):
    match_id = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=100)
    time = models.IntegerField()
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)
    comments = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Event | {self.type} - {self.detail} - {self.team_name} - {self.player_name} | comments {self.comments}'



class NumberOfGamesToPredict(models.Model):
    EPL = models.IntegerField()
    UCL = models.IntegerField()

    def __str__(self) -> str:
        return f'Number of games to predict | EPL = {self.EPL}, UCL = {self.UCL}'