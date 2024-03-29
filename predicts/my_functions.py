import requests
from predicts.models import MatchEvents, MatchPrediction
from predicts.models import Match
import os
from datetime import date, timedelta
import datetime

#date section
# Get the current date
current_date = datetime.date.today()

year, week, day = current_date.isocalendar()

# first_day_of_week = current_date - datetime.timedelta(days=day-1)
first_day_of_week = current_date - datetime.timedelta(days=day+45)
# first_day_of_week = '2022-12-01'

# last_day_of_week = current_date + datetime.timedelta(days=7-day)
last_day_of_week = current_date + datetime.timedelta(days=8-day)
print(f'first day{first_day_of_week}')
print(f'last day{last_day_of_week}')

def get_last_monday_and_next_sunday(current_date):
    # Get the current day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    current_day = current_date.weekday()

    # Calculate the number of days since the previous Monday
    days_since_monday = current_day + 1

    # Subtract the calculated number of days from the current date to get the previous Monday
    last_monday = current_date - timedelta(days=days_since_monday)

    # Calculate the number of days until the next Sunday
    days_until_sunday = 6 - current_day

    # Add the calculated number of days to the current date to get the next Sunday
    next_sunday = current_date + timedelta(days=days_until_sunday)

    return last_monday, next_sunday

last_monday, next_sunday = get_last_monday_and_next_sunday(current_date)

def match_one_x_two(prediction):
    """return 1 X 2 for match"""
    if prediction.match.hTeamScore > prediction.match.aTeamScore:
        match_winner = '1'
    elif prediction.match.hTeamScore == prediction.match.aTeamScore:
        match_winner = 'X'
    elif prediction.match.hTeamScore < prediction.match.aTeamScore:
        match_winner = '2'
    return match_winner

def prediction_one_x_two(prediction):
    """return 1 X 2 for match prediction"""
    if prediction.homeTeamScore > prediction.awayTeamScore:
        prediction_winner = '1'
    elif prediction.homeTeamScore == prediction.awayTeamScore:
        prediction_winner = 'X'
    elif prediction.homeTeamScore < prediction.awayTeamScore:
        prediction_winner = '2'
    return prediction_winner

def single_match_points(match):
    unchacked_predictions = MatchPrediction.objects.filter(match__match_id=match.match_id)
    print(unchacked_predictions)

    for prediction in unchacked_predictions:
        points = 0
        goal_scorers = MatchEvents.objects.filter(match=prediction.match).filter(type='Goal').order_by('time')
        red_cards = MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card')
        print(f'number of red cards: {len(red_cards)}')
   
        if prediction.match.status == 'FT':
            print('Match Finished calculate points')
            #red card minus points
            # if MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card').filter(player=prediction.goalScorer).exists():
            if MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card').filter(team=prediction.goalScorer.team).exists():
            #minus points
                print('minus point for red card')
                points -= 1
            else:
                print('no penalty points for red card')
            
            #goalscorers points
            try:
                if goal_scorers[0].player.name == prediction.goalScorer.name:
                    points+=3
                    print('3 points for correct first goalscorer')
                else:
                  for goal in goal_scorers:
                    if goal.player.name == prediction.goalScorer.name:
                      print('1 point for anytime goalscorer')
                      points +=1
                      break
                    else:
                      continue
            except:
                points += 0
            
            #correct score points
            if prediction.homeTeamScore == prediction.match.hTeamScore and prediction.awayTeamScore == prediction.match.aTeamScore:
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

 
#function to get games
def get_all_games(league_id, season,monday,sunday):
    """get all games"""
    # epl id = 39
    # champions league id = 2
    #serie a id = 135
    #la liga id = 140
    # UEFA Natons League id: 5
    #world cup id: 1
    #MLS id 253

    # url = f'https://v3.football.api-sports.io/fixtures?league=135&season=2022&timezone=Europe/London&from={first_day_of_week}&to={last_day_of_week}'
    url = f'https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}&timezone=Europe/London&from={monday}&to={sunday}'
    # url = 'https://v3.football.api-sports.io/fixtures?league=5&season=2022' # UEFA Natons League

    payload={}
    headers = {
      'x-rapidapi-key': os.environ.get('key','dev default value'),
      'x-rapidapi-host': os.environ.get('host','dev default value'),
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    print(f'request status code:{r.status_code}')
    data = r.json()
    response = data['response']
    # print(response)
    sorted_matches = sorted(response, key=lambda x: x['fixture']['date'])
    print(f"this is lenght of get all games sorted matches {len(sorted_matches)}")
    # print(f'sorted matches {data}')
    return sorted_matches


def get_match_details(match_id):
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
    return response

def get_players(team_id):
    """get players for all teams"""

    url = f'https://v3.football.api-sports.io/players/squads?team={team_id}'
    
    payload={}
    headers = {
      'x-rapidapi-key': os.environ.get('key','dev default value'),
      'x-rapidapi-host': os.environ.get('host','dev default value'),
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    print(f'request status code:{r.status_code}')

    data = r.json()
    players = data['response'][0]['players']
    return players

