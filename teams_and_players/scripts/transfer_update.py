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

    api_team_players_ids = []
    db_team_players_ids = get_db_players_ids(team_id)

    for i in players:
        id = i['id']
        api_team_players_ids.append(id)


# section to update squads and add new players
    for i in players:
        id = i['id']
        name = i['name']
        age = i['age']
        number = i['number']
        position = i['position']
        photo = i['photo']
        team_id = team['id']
        print(f'player id: {id}, name: {name}, team id: {team_id}')

       

        if Player.objects.filter(player_id=id).exists():

            # Player.objects.filter(player_id=id).update(
            # name=name,
            # age=age,
            # number=number,
            # position = position,
            # photo = photo,
            # team = Team.objects.get(id=team_id)
            # )
            print(f'Player {name} is in database.')
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
            print(f'\n NEW Player {name} added to db.\n')
                
# section to transfer out old players to new teams
    players_to_transfer_out = return_players_to_transfer_out(db_team_players_ids,api_team_players_ids)

    print(f'Numbers of players to transfer out: {len(players_to_transfer_out)}')
    counter = len(players_to_transfer_out)
    for p in players_to_transfer_out:
        transfer_out(p)
        left = counter - 1
        print(f'{left} to finish this team transfers')





def get_teams_ids():
    teams = Team.objects.all()
    ids = []
    for team in teams:
        ids.append(team.id)

    return ids

def get_db_players_ids(team_id):
    """return list of players ids for team"""
    id_list = []
    players = Player.objects.filter(team_id = team_id)
    for player in players:
        id_list.append(player.player_id)
    print(f'number of players id for team = {len(id_list)}')
    return id_list

def return_players_to_transfer_out(db_team_players_ids,api_team_players_ids):
        """Return only players who need to be transfer out"""
        players_to_transfer = []
        for x in db_team_players_ids:
            if x not in api_team_players_ids:
                players_to_transfer.append(x)
            else:
                continue
        return players_to_transfer

def transfer_out(player_id):
    """change team of player to transfer out"""

    season = 2022

    url = f'https://v3.football.api-sports.io/players?id={player_id}&season={season}'
    
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
    stats = response[0]['statistics']
    team = stats[0]['team']
    team_id = team['id']

    
    try:
        p = Player.objects.filter(player_id=player_id)
        p.update(
            team = Team.objects.get(id=team_id)
            )
        print(f'\nPlayer updated. and transfer has been done :) \n')
    except:
        Player.objects.filter(player_id=player_id).update(
            team = Team.objects.get(id=999999999)
            )
        print(f'\nPlayer transfered out to N/A team \n')

    print('sleep for 20 sec')
    time.sleep(20)


def get_players_run():
    ids = get_teams_ids()

    for i in ids:
        get_players(i)
        print('sleep for 20 seconds')
        time.sleep(20)
        

    print('all players added to db')



get_players_run()