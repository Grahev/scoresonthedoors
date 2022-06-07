from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.utils import timezone
from django.contrib.auth.models import User
from teams_and_players.models import Team, Player

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
        return f'MD{self.matchday} - {self.hTeam} : {self.aTeam} - {self.status}'

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
        first = MatchEvents.objects.filter(match=self).first()
        try:
            f = first.player.name
        except:
            f = ""
        return f


class MatchPrediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    homeTeamScore = models.PositiveIntegerField()
    awayTeamScore = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalScorer = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    checked = models.BooleanField(default=False)
    points = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'MD:{self.pk}- ID: {self.match_id}-{self.user}- {self.homeTeamScore} : {self.awayTeamScore}'

    @property
    def is_past_due(self):
        return timezone.now() > self.match.date

class MatchEvents(models.Model):
    match = models.ForeignKey(Match, on_delete=DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=DO_NOTHING)
    time = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=DO_NOTHING)
    type = models.CharField(max_length=50)

class MatchEvents(models.Model):
    match = models.ForeignKey(Match, on_delete=DO_NOTHING, related_name='events')
    team = models.ForeignKey(Team, on_delete=DO_NOTHING)
    time = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=DO_NOTHING)
    type = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)

