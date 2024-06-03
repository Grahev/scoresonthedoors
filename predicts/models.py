from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.utils import timezone
from django.contrib.auth.models import User
from django.apps import apps
from predicts.my_functions import get_match_details
import os
import requests
from django.core.cache import cache
from datetime import timedelta, datetime
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
import json
import re
from django.core.cache import cache
# Create your models here.


class Match(models.Model):
    api_url = 'https://www.fotmob.com/api/matchDetails'
    hTeam_name = models.CharField(blank=True, null=True, max_length=100)
    aTeam_name = models.CharField(blank=True, null=True, max_length=100)
    hTeam_id = models.IntegerField(blank=True, null=True)
    aTeam_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    hTeamScore = models.IntegerField(blank=True, null=True)
    aTeamScore = models.IntegerField(blank=True, null=True)
    goalScorers = models.TextField(blank=True, null=True)
    match_id = models.IntegerField(unique=True)
    league = models.CharField(max_length=50, blank=True, null=True)
    league_id = models.IntegerField(blank=True, null=True)
    data = models.TextField(null=True,blank=True)
    onextwo = models.CharField(blank=True, null=True, max_length=1)
    league_sezon = models.CharField(blank=True, null=True, max_length=25)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Match | {self.date} - {self.hTeam_name} : {self.aTeam_name} - {self.finished}'

    def fetch_data(self):

        headers = {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        params = {
        'matchId': self.match_id,
        }
        cache_key = f'match_cache_{self.match_id}'
        data = cache.get(cache_key)

        if not data:
            r = requests.get(self.api_url, params=params, headers=headers)
            if r.status_code == 200:
                data = r.json()
                cache.set(cache_key, data, timeout=3600) #3600 1 hour timeout,  86400 s (24 h * 3600 seconds/hour)
            else:
                data = None
        
        return data
    
    def get_goals(self):
        """return list of goals scorers"""
        goals_data = self.fetch_data()['header']['events']
        # Collect all goal events
        all_goals = []

        if goals_data:
          # Function to extract and append goal details
          def extract_goal_data(team_goals, is_home):
              for player_goals in team_goals.values():
                  for goal in player_goals:
                      goal_data = {
                          'name': goal['player']['name'],
                          'id': goal['player']['id'],
                          'time': goal['time'],
                          'is_home': is_home
                      }
                      all_goals.append(goal_data)


          # Extract home team goals
          extract_goal_data(goals_data['homeTeamGoals'], True)

          # Extract away team goals
          extract_goal_data(goals_data['awayTeamGoals'], False)

          # Sort goals by time
          all_goals.sort(key=lambda x: (x['time'], x.get('overloadTime', 0))) 

          return all_goals
        else:
            all_goals = None

    
    def first_goal(self):
        """return first goalscorer"""
        if self.get_goals():
          return self.get_goals()[0]
        else:
            return None
        
    def get_result(self):
        try:
            score = self.fetch_data()['header']['status']['scoreStr']
        except:
            score = None
        return score
        
    
    def one_x_two(self,home:int,away:int):
        try:
            if home > away:
                return 1
            elif home == away:
                return 0
            elif home < away:
                return 2
            else:
                None
        except:
            None
    
    def match_result(self):
        return self.one_x_two(self.hTeamScore, self.aTeamScore)
    
    def update_match_data(self):
        """fill all match data like home team etc."""
        data = self.fetch_data()
        league_id = data['general']['leagueId']
        league = data['general']['leagueName']
        home_teama_name = data['general']['homeTeam']['name']
        home_teama_id = data['general']['homeTeam']['id']
        away_teama_name = data['general']['awayTeam']['name']
        away_teama_id = data['general']['awayTeam']['id']
        started = data['general']['started']
        finished = data['general']['finished']
        date = data['general']['matchTimeUTCDate']

        if data:
            self.league_id = league_id
            self.league = league
            self.started = started
            self.finished = finished
            if self.first_goal():
                self.match_goalscorer = self.first_goal()['name']
            if self.first_goal():
                self.match_goalscorer_id = self.first_goal()['id']
            if self.get_result():
                self.hTeamScore = int(self.get_result()[0].strip())
                self.aTeamScore = int(self.get_result()[-1].strip())
            self.hTeam_name = home_teama_name
            self.aTeam_name = away_teama_name
            self.hTeam_id = home_teama_id
            self.aTeam_id = away_teama_id
            self.data = data
            if self.match_result():
                self.onextwo = self.match_result()
            self.goalScorers = self.get_goals()
            self.date = date

        self.save()

    @property
    def is_past_due(self):
        return timezone.now() > self.date

    @property
    def is_active(self):
        return timezone.now() < self.date


class MatchPrediction(models.Model):
    homeTeamScore = models.PositiveIntegerField()
    awayTeamScore = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalScorerId = models.IntegerField(default=0)
    goalScorerName = models.CharField(max_length=55)
    checked = models.BooleanField(default=False)
    points = models.IntegerField(blank=True, null=True)
    match = models.ForeignKey(Match, on_delete=CASCADE, related_name='predictions')
    onextwo = models.CharField(max_length=1)
    
    def __str__(self):
        return f'Match Prediction | {self.user} - {self.match.hTeam_name} {self.homeTeamScore} : {self.awayTeamScore} {self.match.aTeam_name}'
    
    def one_x_two(self,home:int,away:int):
        if home > away:
            return 1
        elif home == away:
            return 0
        else:
            return 2

    def match_result(self):
        return self.one_x_two(self.homeTeamScore, self.awayTeamScore)
    
    def calculate_points(self):
        """calculate points"""
        if not self.match.started:
            return 0  # Match not started, points are 0
        
        m_points = 0
        g_points = 0
      
        if self.match.started:
            print('match started calculate points')
            print(f'pred home team score {self.homeTeamScore} - match h team {self.match.hTeamScore}')
            if self.homeTeamScore == self.match.hTeamScore and self.awayTeamScore == self.match.aTeamScore:
                m_points =+ 3
            elif self.onextwo == self.match.onextwo:
                m_points =+1
            if self.match.first_goal():
                if self.goalScorerId == self.match.first_goal()['id']:
                    g_points =+3
                else:
                #   for goal in self.match.goalScorers:
                  for goal in self.match.get_goals():
                    if self.goalScorerId == int(goal['id']):
                        g_points += 1
                        break
            else:
                pass
            points = m_points + g_points
            self.points = points
            self.save()
            return points

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
    