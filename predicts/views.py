from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from hashlib import sha256
import requests
import os
from .forms import ApiMatchPredictionForm, ApiMatchPredictionFormUpdat
from .models import Match, MatchPrediction, NumberOfGamesToPredict, LiveLeague
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from datetime import datetime
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.conf import settings

#import for current week
from datetime import date
import time

# delete view import
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

#my functions import
from .my_functions import single_match_points, get_match_details, get_players, get_euro_games, get_team_squad, get_games_by_date, is_list_of_dicts, get_todays_date,filter_matches_by_leagues

from datetime import timedelta, datetime

from app_core.request_config import HEADERS, COOKIES

today = datetime.now()

live_leagues = LiveLeague.objects.filter(active = True)

LEAGUES_IDS = list(live_leagues.values_list('league_id', flat=True)) # turn league_ids into list
print(LEAGUES_IDS)
# FILTER_DATE = timezone.make_aware(datetime(2024, 8, 10))
FILTER_DATE = settings.FILTER_DATE


def predicts_home(request):
   
    all_day = get_games_by_date(get_todays_date())
    fixtures = filter_matches_by_leagues(all_day,LEAGUES_IDS)
    # print(fixtures)
    
    # fixtures = Match.objects.all()
    for league_name, league_info in fixtures.items():
       
        for f in league_info['matches']:
            match_id = f['id']
            # match_id = f.match_id
            match, created = Match.objects.get_or_create(
                match_id = match_id
            )

            if created:
                match.match_id = match_id
                match.update_match_data()
                match.save()
                print(f'created - {match}')
        

    # Calculate next and previous dates
    d = datetime.now() #todays date data_object
    next_date = d + timedelta(days=1) #add 1 day
    previous_date = d - timedelta(days=1) #subtract 1 day
        
    context={
        'fixtures':fixtures,
        'todays_date':d,
        'next_date':next_date.strftime('%Y%m%d'),
        'previous_date':previous_date.strftime('%Y%m%d')
    }
    return render(request, 'predicts_home.html', context)

def predicts_home_date(request, date):
   
    all_day = get_games_by_date(date)
    # print(all_day)
    fixtures = filter_matches_by_leagues(all_day,LEAGUES_IDS)
    # print(fixtures)


    for league_name, league_info in fixtures.items():
        for f in league_info['matches']:
            match_id = f['id']
            # match_id = f.match_id
            match, created = Match.objects.get_or_create(
                match_id = match_id
            )

            if created:
                match.match_id = match_id
                match.update_match_data()
                match.save()
                print(f'created - {match}')

    # Calculate next and previous dates
    d = datetime.strptime(date, '%Y%m%d') #convert string to date_object
    next_date = d + timedelta(days=1) #add 1 day
    previous_date = d - timedelta(days=1) #subtract 1 day
        
    context={
        'fixtures':fixtures,
        'todays_date':d,
        'next_date':next_date.strftime('%Y%m%d'),
        'previous_date':previous_date.strftime('%Y%m%d')
    }
    return render(request, 'predicts_home.html', context)


def user_predictions(request):
    """this view list all existings user predictions"""
    # user = User.objects.get(pk=pk)
    print('run user_predictions')
    user = request.user

    user_predictions = MatchPrediction.objects.filter(
        user=user,
        match__date__gt = FILTER_DATE
        ).order_by('-match__date')

    # for prediction in user_predictions:
    #     if not prediction.checked:
    #         prediction.onextwo = prediction.one_x_two(prediction.homeTeamScore, prediction.awayTeamScore)
    #         prediction.save()
    #     elif prediction.match.finished:
    #         prediction.calculate_points()
    #         prediction.checked = True
    #         prediction.save()

    context = {
        'user':user,
        'user_predictions':user_predictions,

    }

    return render(request, 'user_predictions.html', context)


def match_prediction(request,pk):

    m = Match.objects.get(match_id=pk)
    m.update_match_data()
    match = cache.get(f'match_cache_{pk}') 
    if not match:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        cache.set(f'match_cache_{pk}', get_match_details(pk),350) #86400 = 24h
        match = cache.get(f'match_cache_{pk}')
        # print(match)

    hteam = m.hTeam_name   
    ateam = m.aTeam_name
    

    match_date = match['general']['matchTimeUTCDate']
    # print(match_date)
   # Define the input string and its format
    input_string = match_date
    input_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    # Use the strptime method to convert the string to a datetime object
    match_datetime_object = datetime.strptime(input_string, input_format) 
    # print(match_datetime_object)

    next_date = match_datetime_object + timedelta(days=0) #add 0 day
    # print(next_date)
    
    
    # cache.delete(f'{hteam}_squad')
    hteam_squad = cache.get(f'{hteam}_squad')
    if not hteam_squad:
        time.sleep(1)
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        #set cache
        cache.set(f'{hteam}_squad', get_team_squad(m.hTeam_id), 86400)
        hteam_squad = cache.get(f'{hteam}_squad')
        # print(f'home team {hteam_squad}\n\n')

    # cache.delete(f'{ateam}_squad')
    ateam_squad = cache.get(f'{ateam}_squad')
    if not ateam_squad:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        cache.set(f'{ateam}_squad', get_team_squad(m.aTeam_id), 86400)
        ateam_squad = cache.get(f'{ateam}_squad')

    squads = ateam_squad + hteam_squad 
    
    # Filter out entries with fallback 'Coach'
    filtered_data = [item for item in squads if item['fallback'] != 'Coach']
   
    # Generate form choices with only player names
    form_choices = [(item['name'], f"{item['name']} - {item['fallback']}") for item in filtered_data]
   

    # Update the choices for the form field
    ApiMatchPredictionForm.base_fields['goalScorerName'].choices = form_choices

    # Create the form instance
    form = ApiMatchPredictionForm()
    form.fields['homeTeamScore'].label = ''
    form.fields['awayTeamScore'].label = ''
    form.fields['goalScorerName'].label = ''

    if request.method == 'POST':
        pred = MatchPrediction.objects.filter(user=request.user).filter(match__match_id=pk).exists()
        # print(pred)
        form = ApiMatchPredictionForm(request.POST)
        if form.is_valid():
            homeTeamScore = form.cleaned_data['homeTeamScore']
            awayTeamScore = form.cleaned_data['awayTeamScore']
            goalScorerName = form.cleaned_data['goalScorerName']
            # Get player ID from the filtered data
            #goalScorerId = next((item['id'] for item in filtered_data if item['name'] == goalScorerName), None)
            # print(goalScorerName)
            
            #get player id from squad json object
            for player in squads:
                if player["name"] == goalScorerName:
                # If the name is found, print the associated id
                    goalScorerId = player["id"] 
                    # print(f"id founded {goalScorerId}")
                else:
                    continue

            if pred == True:
                messages.error(request,'Prediction for this match alerady exists, please make prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            if match['general']['started']:
                messages.error(request,'Prediction match alredy started and can NOT be added on or edited. Please do prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            

            # print(form.cleaned_data)
            
            user = request.user.username
            u = User.objects.get(username=user)
            MatchPrediction.objects.create(
                homeTeamScore=homeTeamScore,
                awayTeamScore=awayTeamScore,
                user = u,
                goalScorerName = goalScorerName,
                goalScorerId = goalScorerId,
                match = Match.objects.get(match_id=pk)
            )
            print('new prediction created')
            return redirect("predicts:predicts-home-date", date=next_date.strftime('%Y%m%d'))


    context = {
        'match':match,
        'form':form,
        'hTeamSquad':hteam_squad,
        'hteam': hteam,
        'ateam': ateam,
        'data': m
        # 'key':key,
    }
    return render(request, 'match_prediction.html', context)

def match_prediction_update(request, pk):
    """Update view for match prediction"""
    pred = get_object_or_404(MatchPrediction, match__match_id=pk, user=request.user)

    hteam_squad = cache.get(f'{pred.match.hTeam_name}_squad')
    if not hteam_squad:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        #set cache
        cache.set(
            #name value in cache table
            f'{pred.match.hTeam_name}_squad', 
            #data 
            get_team_squad(pred.match.match_id), 
            #time out for cache data
            86400)
        hteam_squad = cache.get(f'{pred.match.hTeam_name}_squad')
    
    ateam_squad = cache.get(f'{pred.match.aTeam_name}_squad')
    if not ateam_squad:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        #set cache
        cache.set(
            #name value in cache table
            f'{pred.match.aTeam_name}_squad', 
            #data 
            get_team_squad(pred.match.match_id), 
            #time out for cache data
            86400)
        hteam_squad = cache.get(f'{pred.match.aTeam_name}_squad')
    squads = ateam_squad + hteam_squad
    # Create a list of choices from the dictionary
    # choices = [(player['name'],player['name'] ) for player in squads]

    # Filter out entries with fallback 'Coach'
    filtered_data = [item for item in squads if item['fallback'] != 'Coach']

    # Generate form choices with only player names
    form_choices = [(item['name'], f"{item['name']} - {item['fallback']}") for item in filtered_data]
   

    # Update the choices for the form field
    ApiMatchPredictionFormUpdat.base_fields['goalScorerName'].choices = form_choices



    if request.method == 'POST':
        form = ApiMatchPredictionFormUpdat(request.POST, instance=pred)
        if form.is_valid():
            form.save()
            return redirect('predicts:user_predictions')  # Replace 'success_page' with the desired URL name for the success page
    else:
        form = ApiMatchPredictionFormUpdat(instance=pred)

    context = {'form': form, 'hTeam':pred.match.hTeam_name, 'aTeam':pred.match.aTeam_name, 'match':pred.match.match_id, 'pred':pred}
    return render(request, 'match_prediction_update.html', context)


def delete_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(MatchPrediction, match__match_id = pk, user=request.user)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("predicts:user_predictions")
    
    context["prediction"] = obj
 
    return render(request, "prediction_delete.html", context)

def user_predictions_list(request, user):
    '''
    View for list of user predictions, view from league page
    '''

    predictions = MatchPrediction.objects.filter(
        user__username = user,
        match__date__gt = FILTER_DATE
        ).order_by('match__date')
    context = {
        'predictions': predictions
    }
       
    return render(request, 'user_predictions_list.html', context)


@staff_member_required
def event_delete(request,pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(MatchEvents, id = pk)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("predicts:predicts-home")
    
    context["prediction"] = obj
 
    return render(request, "match_event_delete.html", context)

@staff_member_required
def match_point_update(request, pk):
    """update points for all predictions for single match"""
    match = Match.objects.get(pk=pk)
    single_match_points(match)
    return render(request, 'single_match_points.html')


