import requests
#import config
import os
from teams_and_players.models import Team, Player
from predicts.models import Match, MatchEvents
import time

from datetime import date
current_week = date.today().isocalendar()[1]  # return current week :)




def match_update(event_id):
    print(f'EVENT ID: {event_id}')
    #event_id = '710676'
    url = f'https://v3.football.api-sports.io/fixtures?id={event_id}'

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

    
    hTeamScore = response[0]['goals']['home']
    if hTeamScore:
        print('score not null')
    else:
        hTeamScore = 0
    aTeamScore = response[0]['goals']['away']
    if aTeamScore:
        print('score not null')
    else:
        aTeamScore = 0
    status = response[0]['fixture']['status']['short']
    events = response[0]['events']
    
    #update match score and status
    if status == 'FT':
        m = Match.objects.get(match_id=event_id)
        m.hTeamScore = int(hTeamScore)
        m.aTeamScore = int(aTeamScore)
        m.status = status
        m.save()
        print(f'match scores updated {m}')
    else:
        m = Match.objects.get(match_id=event_id)
        m.status = status
        m.date = response[0]['fixture']['date']
        m.save()
        print('match not finished - date updated.')
    
    #create events for match
    for event in events:
        match_id = event_id
        team_id = event['team']['id']
        time = event['time']['elapsed']
        player_id = event['player']['id']
        e_type = event['type']
        e_detail = event['detail']

        #print(f'match id:{match_id}, team id: {team_id}, time:{time}, player id:{player_id}, type:{e_type}')

        if player_id:
            #print(m)
            try:
                m.goalScorers.add(Player.objects.get(player_id=player_id)) #add goalscorers to match goalscorers (many to many field)
            except:
                m.goalScorers.add(Player.objects.get(player_id=0))
            #create event object with all goals 
            try:
                p = Player.objects.get(player_id=player_id)
            except:
                p = Player.objects.get(player_id=0)

            if e_type == 'Card':
                match_event = MatchEvents.objects.create(
                    match = Match.objects.get(match_id=match_id),
                    team = Team.objects.get(id=team_id),
                    time = time,
                    player = p,
                    type = e_type,
                    detail = e_detail,
                )
                match_event.save()
                print('Card event created')
            elif e_type == 'Goal':
                match_event = MatchEvents.objects.create(
                    match = Match.objects.get(match_id=match_id),
                    team = Team.objects.get(id=team_id),
                    time = time,
                    player = p,
                    type = e_type,
                    detail = e_detail,
                )
                match_event.save()
                print('Goal event created')
            else:
                continue
                
        else:
            continue
        


def run():
    all_matches = Match.objects.filter(status='NS').order_by('matchday')

    print(all_matches)

    current_matchday = all_matches.filter(date__week=current_week) #get queryset only for last not finished matchday

    for match in current_matchday:
        if match.status == 'NS':
            match_update(match.match_id)
            print('match updated')
        else:
            continue
        
        print('sleep for 15 seconds')
        time.sleep(15)
        