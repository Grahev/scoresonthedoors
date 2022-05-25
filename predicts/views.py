from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
import requests
import config
from .forms import MatchPredictionForm



def predicts_home(request):
    return render(request, 'predicts_home.html')

@cache_page(60 * 15)
def predicts_list(request,league,year):
    url = f"https://v3.football.api-sports.io/fixtures?league={league}&season={year}"

    payload={}
    headers = {
        'x-rapidapi-key': config.key,
        'x-rapidapi-host': config.host
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    parameters = response.json()
    print(response)


    context = {
        'fixtures':parameters['response'],
        'league': league,
        'year':year
    }
    return render(request,'test.html', context)


def match_prediction(request,league,year,match_id):
    url = f"https://v3.football.api-sports.io/fixtures?league={match_id}"

    payload={}
    headers = {
        'x-rapidapi-key': config.key,
        'x-rapidapi-host': config.host
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    parameters = response.json()
    print(response)
    #need form
    form = MatchPredictionForm(request.POST)
    #need home team
    #need away team
    #need home team squad list
    #need away team squad list

    #need match date and time to validate 
    #need match day to validate it's only 3 predictions
    #need query db to check if prediction exist
    return render(request, 'prediction_create.html')