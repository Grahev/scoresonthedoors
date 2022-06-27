import requests
#import config
from teams_and_players.models import Player, Team
import json
import time
import os


def get_players(team_id):
    """get players for all teams"""

    url = f'https://v3.football.api-sports.io/players/squads?team={team_id}'
    
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
    players= response[0]['players']
    team = response[0]['team']

    for i in players:
        id = i['id']
        name = i['name']
        age = i['age']
        number = i['number']
        position = i['position']
        photo = i['photo']
        team_id = team['id']
        print(f'player id: {id}, name: {name}, team id: {team_id}, age: {age}, number: {number}, position: {position}, photo url: {photo}')

        if Player.objects.filter(player_id=id).exists():

            Player.objects.filter(player_id=id).update(
                name=name,
                age=age,
                number=number,
                position = position,
                photo = photo,
                team = Team.objects.get(id=team_id)
            )
            print(f'Player {name} updated.')
        else:
            player = Player.objects.create(
            player_id=id,
            name=name,
            age=age,
            number=number,
            position = position,
            photo = photo,
            team = Team.objects.get(id=team_id)
            )
            player.save()
            print(f'Player {name} added to db.')


def get_teams_ids():
    teams = Team.objects.all()
    ids = []
    for team in teams:
        ids.append(team.id)

    return ids

def get_players_run():
    ids = get_teams_ids()

    for i in ids:
        get_players(i)
        print('sleep for 20 seconds')
        time.sleep(20)
        

    print('all players added to db')

get_players_run()