#import config
import requests
from teams_and_players.models import Team
import json
import os

# Premier League id: 39
# UEFA Natons League id: 5
# Champions League id: 2
#World Cup id: 1

def get_teams():
    """get all teams and add them to Team model in database"""

    url = 'https://v3.football.api-sports.io/teams?league=1&season=2022'
    # url = 'https://v3.football.api-sports.io/teams?league=5&season=2022' #nations league url
    
    payload={}
    headers = {
      # 'x-rapidapi-key': config.key,
      # 'x-rapidapi-host': config.host

      'x-rapidapi-key': os.environ.get('key','dev default value'),
      'x-rapidapi-host': os.environ.get('host','dev default value'),

      
    }

    r = requests.request("GET", url, headers=headers, data=payload)

    data = r.json()

    response = data['response']
    print(response)

    for i in response:
        id = i['team']['id']
        name = i['team']['name']
        country = i['team']['country']
        founded = i['team']['founded']
        logo = i['team']['logo']
        team = Team.objects.create(id=id,name=name,country=country,founded=founded,logo=logo)
        team.save()
        print(f'{name} created and saved in database')
        


get_teams()