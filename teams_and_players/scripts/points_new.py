import requests
import os
import time
from django.core.cache import cache

from predicts.models import MatchPrediction, MatchResult, MatchEvents

def compare_ints(a, b):
  if a > b:
    return 1
  elif a == b:
    return "X"
  else:
    return 2

def match_result(match_id):

    if MatchResult.objects.filter(match_id=match_id).exists():
        print('Result alerady exist')
    else:
        url = f'https://v3.football.api-sports.io/fixtures?id={match_id}'

        payload={}
        headers = {
          'x-rapidapi-key': os.environ.get('key','dev default value'),
          'x-rapidapi-host': os.environ.get('host','dev default value'),
        }
        r = requests.request("GET", url, headers=headers, data=payload)
        print(f'request status code:{r.status_code}')
        data = r.json()
        response = data['response']
        status = response[0]['fixture']['status']['long'] # Match Finished
        events = response[0]['events']
        homeTeamResult = response[0]['goals']['home']
        awayTeamResult = response[0]['goals']['away']
        

        if status == 'Match Finished':
            resultCode = compare_ints(homeTeamResult,awayTeamResult)
            print('match finished')
            match_result = MatchResult.objects.create(
                match_id = match_id,
                homeTeamResult = response[0]['goals']['home'],
                awayTeamResult = response[0]['goals']['away'],
                resultCode = resultCode
                # firstGoalScorerId = 
                # firstGoalScorerName = 
            )
            match_result.save()
            print(match_result)
        else:
            print('not finished')

def create_match_events(match_id):
        #check if any events exists
        print(type(match_id))
        # existing_events = MatchEvents.objects.filter(match_id == match_id)

        # if len(existing_events) > 1 :
        if MatchEvents.objects.filter(match_id = match_id).exists():
            
            print('Events alerady exists')
        
        else:
            print('events not exists')
            url = f'https://v3.football.api-sports.io/fixtures?id={match_id}'

            payload={}
            headers = {
              'x-rapidapi-key': os.environ.get('key','dev default value'),
              'x-rapidapi-host': os.environ.get('host','dev default value'),
            }
            r = requests.request("GET", url, headers=headers, data=payload)
            print(f'request status code:{r.status_code}')

            data = r.json()

            response = data['response']

            status = response[0]['fixture']['status']['long'] # Match Finished
            events = response[0]['events']

    
            if status == 'Match Finished':
            
                #create events for match
                for event in events:
                    match_id = match_id
                    team_id = event['team']['id']
                    team_name = event['team']['name']
                    time = event['time']['elapsed']
                    player_id = event['player']['id']
                    player_name = event['player']['name']
                    e_type = event['type']
                    e_detail = event['detail']
                    e_comments = event['comments']

                    #print(f'match id:{match_id}, team id: {team_id}, time:{time}, player id:{player_id}, type:{e_type}')

                    if player_id:

                        if e_type == 'Card':
                            match_event = MatchEvents.objects.create(
                                match_id = match_id,
                                team_id = team_id,
                                team_name = team_name,
                                time = time,
                                player_id = player_id,
                                player_name = player_name,
                                type = e_type,
                                detail = e_detail,
                                comments = e_comments
                            )
                            match_event.save()
                            print('Card event created')
                        elif e_type == 'Goal':
                            match_event = MatchEvents.objects.create(
                                match_id = match_id,
                                team_id = team_id,
                                team_name = team_name,
                                time = time,
                                player_id = player_id,
                                player_name = player_name,
                                type = e_type,
                                detail = e_detail,
                                comments = e_comments
                            )
                            match_event.save()
                            print('Goal event created')
                        else:
                            continue

                    else:
                        print(f'Event player id not exist - skip and go to next event | event type: {e_type} details:{e_detail}')


def single_match_points(match_id):
    points = 0
    unchacked_predictions = MatchPrediction.objects.filter(match_id=match_id)
    goal_scorers = MatchEvents.objects.filter(match_id=match_id).filter(type='Goal').order_by('time')
    red_cards = MatchEvents.objects.filter(match_id=match_id).filter(detail='Red Card')
    print(f'number of red cards: {len(red_cards)}')

    match_result = MatchResult.objects.filter(match_id=match_id)

    for prediction in unchacked_predictions:

        if MatchResult.objects.filter(match_id=match_id).exists():
                print('Match Finished calculate points')
                #red card minus points
                # if MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card').filter(player=prediction.goalScorer).exists():
                # if MatchEvents.objects.filter(match_id=match_id).filter(detail='Red Card').filter(team_id=match_result.team_id).exists():
                #minus points
                #     print('minus point for red card')
                #     points -= 1
                # else:
                #     print('no penalty points for red card')

                #goalscorers points
                try:
                    if goal_scorers[0].player_id == prediction.goalScorerId:
                        points+=3
                        print('3 points for correct first goalscorer')
                    else:
                      for goal in goal_scorers:
                        if goal.player_id == prediction.goalScorerId:
                          print('1 point for anytime goalscorer')
                          points +=1
                          break
                        else:
                          continue
                except:
                    points += 0

                #correct score points
                if prediction.homeTeamScore == match_result.homeTeamResult and prediction.awayTeamScore == match_result.awayTeamResult:
                    points +=3
                    print('3 points for correct score')
                
                #winning team points
                else: 
                    match_winner = match_one_x_two(prediction)
                    prediction_winner = prediction_one_x_two(prediction)
                    if match_winner == prediction_winner:
                        points +=1
                        print('1 point for winner')
                    else:
                        points +=0



                p = MatchPrediction.objects.filter(pk=prediction.pk)
                p.update(points=points, checked=True)
                print(f'points: {points} - {p} updated')


            else:
                print('match status not finished')
    


def run():
    fixtures = cache.get('fixtures_cache')
    for fixture in fixtures:

        match_id = fixture['fixture']['id']
        status = fixture['fixture']['status']['long']

        if status =='Match Finished':

            print(f'\n\n{match_id} \n\n')

            match_result(match_id)
            create_match_events(match_id)
            print('Sleep for 10 seconds')
            time.sleep(10)
        else:
            continue
    print('finish')
