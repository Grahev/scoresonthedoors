import requests
#from predicts.models import MatchEvents, MatchPrediction
# from predicts.models import Match
import os
from datetime import date, timedelta, datetime
import datetime
from datetime import datetime
import json
import time
from django.http import JsonResponse

# Get the current date
# current_date = datetime.date.today()

# year, week, day = current_date.isocalendar()

# # first_day_of_week = current_date - datetime.timedelta(days=day-1)
# first_day_of_week = current_date - datetime.timedelta(days=day+45)


# last_day_of_week = current_date + datetime.timedelta(days=8-day)


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

# last_monday, next_sunday = get_last_monday_and_next_sunday(current_date)

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
    match.calculate_points()

 

def get_games_by_date(date=None):
    """pass date in format YYYMMDD"""
    # Get the current date and time
    
    cookies = {
        '_hjSessionUser_2585474': 'eyJpZCI6IjQ5MzQ4M2E3LTljN2ItNTY0Mi04ZTlkLTllNDBhNGU5Njc3NSIsImNyZWF0ZWQiOjE2NDk4NzM4MTQyODEsImV4aXN0aW5nIjp0cnVlfQ==',
        'NEXT_LOCALE': 'en-GB',
        '_ga': 'GA1.2.1094432626.1649006611',
        '_ga_SQ24F7Q7YW': 'GS1.1.1708259313.13.0.1708259314.0.0.0',
        '_ga_K2ECMCJBFQ': 'GS1.1.1708259313.12.0.1708259314.0.0.0',
        '_ga_G0V1WDW9B2': 'GS1.1.1708299288.79.1.1708299757.52.0.0',
        'g_state': '{"i_p":1712784070517,"i_l":4}',
        'u:location': '%7B%22countryCode%22%3A%22GB%22%2C%22ccode3%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%2C%22ip%22%3A%2286.150.110.98%22%2C%22regionId%22%3A%22NIR%22%2C%22regionName%22%3A%22Northern%20Ireland%22%7D',
        'spotim_visitId': '{%22creationDate%22:%22Tue%20May%2021%202024%2020:11:35%20GMT+0100%20(British%20Summer%20Time)%22%2C%22duration%22:1}',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,pl;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': '_hjSessionUser_2585474=eyJpZCI6IjQ5MzQ4M2E3LTljN2ItNTY0Mi04ZTlkLTllNDBhNGU5Njc3NSIsImNyZWF0ZWQiOjE2NDk4NzM4MTQyODEsImV4aXN0aW5nIjp0cnVlfQ==; NEXT_LOCALE=en-GB; _ga=GA1.2.1094432626.1649006611; _ga_SQ24F7Q7YW=GS1.1.1708259313.13.0.1708259314.0.0.0; _ga_K2ECMCJBFQ=GS1.1.1708259313.12.0.1708259314.0.0.0; _ga_G0V1WDW9B2=GS1.1.1708299288.79.1.1708299757.52.0.0; g_state={"i_p":1712784070517,"i_l":4}; u:location=%7B%22countryCode%22%3A%22GB%22%2C%22ccode3%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%2C%22ip%22%3A%2286.150.110.98%22%2C%22regionId%22%3A%22NIR%22%2C%22regionName%22%3A%22Northern%20Ireland%22%7D; spotim_visitId={%22creationDate%22:%22Tue%20May%2021%202024%2020:11:35%20GMT+0100%20(British%20Summer%20Time)%22%2C%22duration%22:1}',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        # 'referer': 'https://www.fotmob.com/en-GB/leagues/50/matches/euro?page=1',
        'referer': 'https://www.fotmob.com/en-GB?date=20240604&show=all&filter=&q=Friendlies',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-fm-req': 'eyJib2R5Ijp7ImNvZGUiOjE3MTYzMTkwOTc5MTZ9LCJzaWduYXR1cmUiOiIwQTI1QTY3MEMyOEREQzc4NzY5NTAyNjAzMTRDNThEMyJ9',
    }

    params = {
        'date': date,
        'ccode3': 'GBR',
    }
    response = requests.get('https://www.fotmob.com/api/matches', params=params, cookies=cookies, headers=headers)
    data = response.json()['leagues']
    pretty_json = json.dumps(data, indent=4)
    # print(pretty_json)


    return data

def is_list_of_dicts(data):
    """Ceck if input data is a list of dictionaries"""
    return isinstance(data, list) and all(isinstance(item, dict) for item in data)


def get_match_details(match_id):
    url = f'https://www.fotmob.com/api/matchDetails'
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    params = {
    'matchId': match_id,
    }
    r = requests.get(url, params=params, headers=headers)
    response = r.json()
    return response


def get_team_squad(id,ccode3="GBR"):
    url = f'https://www.fotmob.com/api/teams'
    headers = {
        'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,pl;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': '_hjSessionUser_2585474=eyJpZCI6IjQ5MzQ4M2E3LTljN2ItNTY0Mi04ZTlkLTllNDBhNGU5Njc3NSIsImNyZWF0ZWQiOjE2NDk4NzM4MTQyODEsImV4aXN0aW5nIjp0cnVlfQ==; NEXT_LOCALE=en-GB; _ga=GA1.2.1094432626.1649006611; _ga_SQ24F7Q7YW=GS1.1.1708259313.13.0.1708259314.0.0.0; _ga_K2ECMCJBFQ=GS1.1.1708259313.12.0.1708259314.0.0.0; _ga_G0V1WDW9B2=GS1.1.1708299288.79.1.1708299757.52.0.0; g_state={"i_p":1712784070517,"i_l":4}; u:location=%7B%22countryCode%22%3A%22GB%22%2C%22ccode3%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%2C%22ip%22%3A%2286.150.110.98%22%2C%22regionId%22%3A%22NIR%22%2C%22regionName%22%3A%22Northern%20Ireland%22%7D; spotim_visitId={%22creationDate%22:%22Wed%20Jun%2005%202024%2017:37:00%20GMT+0100%20(British%20Summer%20Time)%22%2C%22duration%22:1}',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.fotmob.com/en-GB/teams/8497/squad/slovakia',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-fm-req': 'eyJib2R5Ijp7ImNvZGUiOjE3MTc2MDU0NjIzNzN9LCJzaWduYXR1cmUiOiI3NTkwOEFEQjBEODY1NDdFNjFDRjZDN0FDM0NGRjEzMiJ9',
    }
    params = {
    'id': id,
    'ccode3': ccode3,
}
    r = requests.get(url, params=params, headers=headers)
    
    if r.status_code ==200:
        response = r.json()['squad']
        team = convert_to_player_list(response)
        
        return team
    else:
        return None


def convert_to_player_list(squad_json):
    player_list = []
  
    if not squad_json:
        return player_list
    
    for group in squad_json:
        title = group.get('title', '')
        members = group.get('members', [])
        
        for member in members:
            player = {
                'id': member['id'],
                'fallback': member['role']['fallback'],
                'name': member['name'],
                # Uncomment the following lines if the fields are present in the JSON
                # 'rating': member.get('rating', None),
                # 'goals': member.get('goals', 0),
                # 'assists': member.get('assists', 0),
                # 'ycards': member.get('ycards', 0)
            }
            player_list.append(player)

    if is_list_of_dicts(player_list):
        print('is list of dict')
        return player_list
    else:
        print('is not a list of dict!!!')
        return None


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


def get_euro_games():
    cookies = {
        '_hjSessionUser_2585474': 'eyJpZCI6IjQ5MzQ4M2E3LTljN2ItNTY0Mi04ZTlkLTllNDBhNGU5Njc3NSIsImNyZWF0ZWQiOjE2NDk4NzM4MTQyODEsImV4aXN0aW5nIjp0cnVlfQ==',
        'NEXT_LOCALE': 'en-GB',
        '_ga': 'GA1.2.1094432626.1649006611',
        '_ga_SQ24F7Q7YW': 'GS1.1.1708259313.13.0.1708259314.0.0.0',
        '_ga_K2ECMCJBFQ': 'GS1.1.1708259313.12.0.1708259314.0.0.0',
        '_ga_G0V1WDW9B2': 'GS1.1.1708299288.79.1.1708299757.52.0.0',
        'g_state': '{"i_p":1712784070517,"i_l":4}',
        'u:location': '%7B%22countryCode%22%3A%22GB%22%2C%22ccode3%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%2C%22ip%22%3A%2286.150.110.98%22%2C%22regionId%22%3A%22NIR%22%2C%22regionName%22%3A%22Northern%20Ireland%22%7D',
        'spotim_visitId': '{%22creationDate%22:%22Tue%20May%2021%202024%2020:11:35%20GMT+0100%20(British%20Summer%20Time)%22%2C%22duration%22:1}',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,pl;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': '_hjSessionUser_2585474=eyJpZCI6IjQ5MzQ4M2E3LTljN2ItNTY0Mi04ZTlkLTllNDBhNGU5Njc3NSIsImNyZWF0ZWQiOjE2NDk4NzM4MTQyODEsImV4aXN0aW5nIjp0cnVlfQ==; NEXT_LOCALE=en-GB; _ga=GA1.2.1094432626.1649006611; _ga_SQ24F7Q7YW=GS1.1.1708259313.13.0.1708259314.0.0.0; _ga_K2ECMCJBFQ=GS1.1.1708259313.12.0.1708259314.0.0.0; _ga_G0V1WDW9B2=GS1.1.1708299288.79.1.1708299757.52.0.0; g_state={"i_p":1712784070517,"i_l":4}; u:location=%7B%22countryCode%22%3A%22GB%22%2C%22ccode3%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%2C%22ip%22%3A%2286.150.110.98%22%2C%22regionId%22%3A%22NIR%22%2C%22regionName%22%3A%22Northern%20Ireland%22%7D; spotim_visitId={%22creationDate%22:%22Tue%20May%2021%202024%2020:11:35%20GMT+0100%20(British%20Summer%20Time)%22%2C%22duration%22:1}',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.fotmob.com/en-GB/leagues/50/matches/euro?page=1',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-fm-req': 'eyJib2R5Ijp7ImNvZGUiOjE3MTYzMTkwOTc5MTZ9LCJzaWduYXR1cmUiOiIwQTI1QTY3MEMyOEREQzc4NzY5NTAyNjAzMTRDNThEMyJ9',
    }

    params = {
        'id': '50',
        # 'id': '45',
        'ccode3': 'GBR',
    }

    response = requests.get('https://www.fotmob.com/api/leagues', params=params, cookies=cookies, headers=headers)
    data = response.json()['overview']['leagueOverviewMatches']

    return data

# def filter_matches_by_leagues(leagues, league_ids):
#     """
#     Filters matches from the list of leagues based on the provided league IDs.

#     Args:
#         leagues (list): The list of league dictionaries containing match information.
#         league_ids (list): A list of league IDs to filter the matches by.

#     Returns:
#         list: A list of matches that belong to the specified league IDs.
#     """
#     filtered_matches = []
    
#     for league in leagues:
#         print(league)
#         print(f'{league["ccode"]} - {league["id"]} {league["name"]}')
#         if league['id'] in league_ids:
#             matches = league.get('matches', [])
#             for match in matches:
#                 filtered_matches.append(match)
                
#     return filtered_matches

def filter_matches_by_leagues(leagues, league_ids):
    """
    Filters matches from the list of leagues based on the provided league IDs
    and groups the matches by their respective league names.

    Args:
        leagues (list): The list of league dictionaries containing match information.
        league_ids (list): A list of league IDs to filter the matches by.

    Returns:
        dict: A dictionary where keys are league names and values are lists of matches belonging to those leagues.
    """
    filtered_matches_by_league_name = {}
    
    for league in leagues:
        l={}
        if league['id'] in league_ids:
            league_name = league['name']
            matches = league.get('matches', [])
            
            #add filtered matches to dictionary with league name as key
            l['name']=league_name
            l['matches']=matches
            filtered_matches_by_league_name[league_name] = l
        
    
    return filtered_matches_by_league_name

def get_todays_date():
    return datetime.now().strftime('%Y%m%d')

# f =get_games_by_date("20240810")
# for league in f:
#     print(league.get('id'))
#     print(league.get('name'))