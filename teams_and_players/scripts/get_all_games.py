import requests
#import config
import os
from teams_and_players.models import Player, Team
from predicts.models import Match
import json
import time


def get_all_games():
    """get all games"""
    # epl id = 39
    # champions league id = 2
    #serie a id = 135
    #la liga id = 140
    # UEFA Natons League id: 5
    #world cup id: 1

    url = 'https://v3.football.api-sports.io/fixtures?league=1&season=2022&timezone=Europe/London&status=NS'
    # url = 'https://v3.football.api-sports.io/fixtures?league=1&season=2022'
    # url = 'https://v3.football.api-sports.io/fixtures?league=5&season=2022' # UEFA Natons League
    
    payload={}
    headers = {
    #   'x-rapidapi-key': config.key,
    #   'x-rapidapi-host': config.host

      'x-rapidapi-key': os.environ.get('key','dev default value'),
      'x-rapidapi-host': os.environ.get('host','dev default value'),
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    print(f'request status code:{r.status_code}')


    data = r.json()

    response = data['response']
    match= response[0]['fixture']
    teams = response[0]['teams']
    league = response[0]['league']['name']
    
    
    for match in response:
        matchday = match['league']['round']
        hTeam = match['teams']['home']['id']
        aTeam = match['teams']['away']['id']
        date = match['fixture']['date']
        status = match['fixture']['status']['short']
        hTeamScore = match['goals']['home']
        aTeamScore = match['goals']['away']
        match_id = match['fixture']['id']

        match = Match.objects.create(
            matchday = matchday,
            hTeam = Team.objects.get(id=hTeam),
            aTeam = Team.objects.get(id=aTeam),
            date = date,
            status = status,
            hTeamScore = hTeamScore,
            aTeamScore = aTeamScore,
            match_id = match_id,
            league=league
        )
        match.save()
        print(f'{hTeam} : {aTeam} status: {status} added to db')

def run():
    get_all_games()