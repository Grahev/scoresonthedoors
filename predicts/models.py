from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.utils import timezone
from django.contrib.auth.models import User
from teams_and_players.models import Team, Player
import os
import requests
from django.core.cache import cache
from datetime import timedelta

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
    
    def fetch_match_details(self):
        # Check if match details are already cached
        cache_key = f"match_details_{self.matchApiId}"
        match_details = cache.get(cache_key)

        if match_details is None:
            # Fetch match details from the external API
            # Adjust the API endpoint and parameters according to your needs
            url = f'https://v3.football.api-sports.io/fixtures?id={self.matchApiId}'
            payload={}
            headers = {
                'x-rapidapi-key': os.environ.get('key','dev default value'),
                'x-rapidapi-host': os.environ.get('host','dev default value'),
            }
            r = requests.request("GET", url, headers=headers, data=payload)
            data = r.json()
            match_details = data['response']

            # Determine the cache timeout based on the match status
            status = match_details[0]['fixture']['status']['short']
            print(status)
            if status == 'FT':
                cache_timeout = timedelta(days=180)  # Cache for 6 months for finished matches
                print(cache_timeout)
            else:
                cache_timeout = timedelta(hours=2)  # Cache for 1 hour for ongoing matches

            # Cache the match details with the appropriate timeout
            cache.set(cache_key, match_details, timeout=cache_timeout.total_seconds())

        return match_details

    def home_team_score(self):
        match_details = self.fetch_match_details()[0]
        home_team_score = match_details.get('score', {}).get('fulltime', {}).get('home')
        if home_team_score is None:
            return 'TBC'
        else:
            return home_team_score

    def get_away_team_details(self):
        match_details = self.fetch_match_details()
        away_team_details = match_details.get('away_team', {})
        return away_team_details
    
    def first_goal_scorer(self):
        match_details = self.fetch_match_details()

        data = match_details[0]
        # Retrieve the events from the match details
        events = data.get('events', [])

        # Iterate over the events to find the first goal event
        for event in events:
            if event.get('type') == 'Goal':
                first_goal_scorer = event.get('player', {}).get('name')

        return first_goal_scorer

    def is_correct_score(self):
        match_details = self.fetch_match_details()[0]
        home_team_score = match_details.get('score', {}).get('fulltime', {}).get('home')
        away_team_score = match_details.get('score', {}).get('fulltime', {}).get('away')
        return (
            self.homeTeamScore == home_team_score and
            self.awayTeamScore == away_team_score
        )

    def is_correct_result(self):
        match_details = self.fetch_match_details()[0]
        home_team_score = match_details.get('score', {}).get('fulltime', {}).get('home')
        away_team_score = match_details.get('score', {}).get('fulltime', {}).get('away')

        if home_team_score > away_team_score:
            return self.homeTeamScore > self.awayTeamScore
        elif home_team_score < away_team_score:
            return self.homeTeamScore < self.awayTeamScore
        else:
            return self.homeTeamScore == self.awayTeamScore

    def is_correct_first_goal_scorer(self):
        match_details = self.fetch_match_details()

        data = match_details[0]
        # Retrieve the events from the match details
        events = data.get('events', [])

        # Iterate over the events to find the first goal event
        for event in events:
            if event.get('type') == 'Goal':
                first_goal_scorer = event.get('player', {}).get('name')
                if first_goal_scorer == self.goalScorerName:
                    return True
                else:
                    return False

        return False  # Return False if no goal event is found
    
    def does_first_goal_scorer_score_anytime(self):
        match_details = self.fetch_match_details()
        data = match_details[0]
        # Retrieve the events from the match details
        events = data.get('events', [])

        # Find the first goal scorer
        first_goal_scorer = None
        for event in events:
            if event.get('type') == 'Goal':
                first_goal_scorer = event.get('player', {}).get('name')
                break

        if first_goal_scorer == self.goalScorerName:
            # Check if the first goal scorer scores anytime
            for event in events:
                if event.get('type') == 'Goal':
                    scorer_name = event.get('player', {}).get('name')
                    if scorer_name == first_goal_scorer:
                        return True

        return False  # Return False if the first goal scorer doesn't score anytime
    
    def calculate_points(self):
        points = 0
        # Check if the prediction has the correct score
        if self.is_correct_score():
            points += 3
        # Check if the prediction has the correct result
        if self.is_correct_result() and self.is_correct_score() == False:
            points += 1
        # Check if the prediction has the correct first goal scorer
        if self.is_correct_first_goal_scorer():
            points += 3
        # Check if the first goal scorer in the prediction scores anytime
        if self.does_first_goal_scorer_score_anytime() and self.is_correct_first_goal_scorer() == False:
            print('first goal scorer scores anytime')
            points += 1
        return points
        
    
    def update_points(self):
        points = self.calculate_points()
        self.points = points
        self.save()

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
    


class LiveLeague(models.Model):
    league_id = models.IntegerField()
    league_name = models.CharField(max_length=100)
    league_logo = models.CharField(max_length=100)
    season = models.IntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Live League | {self.league_name} - {self.season}'
    
    def api_url(self):
        return f'https://v3.football.api-sports.io/fixtures?league={self.league_id}&season={self.season}&timezone=Europe/London'
                # https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023&timezone=Europe/London&from={last_monday}&to={next_sunday}