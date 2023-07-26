from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from hashlib import sha256
import requests
import os
from .forms import ApiMatchPredictionForm, ApiMatchPredictionFormUpdat
from .models import Match, MatchPrediction, NumberOfGamesToPredict, Player, MatchEvents, Team, LiveLeague
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from datetime import datetime
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

#import for current week
from datetime import date
current_week = date.today().isocalendar()[1]  # return current week :)
# delete view import
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

#my functions import
from .my_functions import single_match_points, get_all_games, get_match_details, get_players

  # epl id = 39
    # champions league id = 2
    #serie a id = 135
    #la liga id = 140
    # UEFA Natons League id: 5
    #world cup id: 1
    #MLS id 253
    #club frendlies id: 667

def predicts_home(request):
    # cache.delete('ucl_fixtures_cache')
    live_league = LiveLeague.objects.filter(active = True)
    print(live_league)
    numbers_of_games_to_predict = NumberOfGamesToPredict.objects.first()
    ucl_predictions = MatchPrediction.objects.filter(user=request.user).filter(league='UEFA Champions League').filter(match_date__week=current_week).count()
    non_ucl_predictions = MatchPrediction.objects.filter(user=request.user).exclude(league='UEFA Champions League').filter(match_date__week=current_week).count()
    available_non_ucl_predictions = numbers_of_games_to_predict.EPL - non_ucl_predictions
    fixtures = {}
    
    for league in live_league:
        # cache.delete(f'{league.league_name}_cache')
        print(league.league_id)

        league_fixtures = cache.get(f'{league.league_name}_cache') #current week only
        if not league_fixtures:
            print(f'REQUEST TO API! {league} ')
            cache.set(f'{league.league_name}_cache', get_all_games(league.league_id, league.season),86400) #86400 = 24h
            fixtures_league = cache.get(f'{league.league_name}_cache')
            
        else:
            fixtures_league = cache.get(f'{league.league_name}_cache')
            

        fixtures[league.league_name] = fixtures_league
        
        
    

    # if not fixtures:
    #     print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
    #     cache.set('fixtures_cache', get_all_games(253),86400) #86400 = 24h
    #     fixtures = cache.get('fixtures_cache')
    #     print(fixtures)

    # if not ucl_fixtures:
    #     print(' UCL REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
    #     ucl_fixtures = ['ucl_fixtures']
    #     print(ucl_fixtures)
    #     if ucl_fixtures is None:
    #         print('ucl_fixtures is None')
    #         cache.set('ucl_fixtures_cache', ucl_fixtures,86400)
    #     else:
    #         cache.set('ucl_fixtures_cache', get_all_games(2),86400)
    #         ucl_fixtures = cache.get('ucl_fixtures_cache')
        
    context={
        'fixtures':fixtures,
        # 'ucl_fixtures':ucl_fixtures,
        'numbers_of_games_to_predict':numbers_of_games_to_predict,
        'ucl_predictions':ucl_predictions,
        'non_ucl_predictions':non_ucl_predictions,
        'available_non_ucl_predictions':available_non_ucl_predictions,
    }
    return render(request, 'predicts_home.html', context)




# def match_prediction(request):

#     return render(request, 'prediction_create.html')


def user_predictions(request):
    """this view list all existings user predictions"""
    # user = User.objects.get(pk=pk)
    user = request.user

    user_predictions = MatchPrediction.objects.filter(user=user).order_by('-match_date')

    context = {
        'user':user,
        'user_predictions':user_predictions,

    }

    return render(request, 'user_predictions.html', context)


def match_prediction(request,pk):
    
    match = cache.get(f'match_cache_{pk}') 
    if not match:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        cache.set(f'match_cache_{pk}', get_match_details(pk),86400)
        match = cache.get(f'match_cache_{pk}')

    hteam = match[0]['teams']['home']['name']
    ateam = match[0]['teams']['away']['name']
    match_league = match[0]['league']['name']

    match_date = match[0]['fixture']['date']
   # Define the input string and its format
    input_string = match_date
    input_format = '%Y-%m-%dT%H:%M:%S%z'

    # Use the strptime method to convert the string to a datetime object
    match_datetime_object = datetime.strptime(input_string, input_format) 
    print(type(match_datetime_object))
    
    
    # cache.delete(f'{ateam}_squad')
    hteam_squad = cache.get(f'{hteam}_squad')
    if not hteam_squad:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        #set cache
        cache.set(
            #name value in cache table
            f'{hteam}_squad', 
            #data 
            get_players(match[0]['teams']['home']['id']), 
            #time out for cache data
            86400)
        hteam_squad = cache.get(f'{hteam}_squad')

    ateam_squad = cache.get(f'{ateam}_squad')
    if not ateam_squad:
        print('REQUEST TO API!!!!!!!!!!!!!!!!!!!!!')
        cache.set(f'{ateam}_squad', get_players(match[0]['teams']['away']['id']), 86400)
        ateam_squad = cache.get(f'{ateam}_squad')

    squads = ateam_squad + hteam_squad
    
 
    # Create a list of choices from the dictionary
    choices = [(player['name'],player['name'] ) for player in squads]
   

    # Update the choices for the form field
    ApiMatchPredictionForm.base_fields['goalScorerName'].choices = choices

    # Create the form instance

    form = ApiMatchPredictionForm()
    form.fields['homeTeamScore'].label = ''
    form.fields['awayTeamScore'].label = ''
    form.fields['goalScorerName'].label = ''

   
    key = os.environ.get('key')
    #no of games to predict - this store UCL and NON UCL games
    number_of_games_to_predict = NumberOfGamesToPredict.objects.get(pk=1)
    #number of existing user predictions for current week NON UCL
    non_UCL_predictions = MatchPrediction.objects.filter(user = request.user).exclude(league__icontains= 'UEFA Champions League').filter(match_date__week=current_week).count()
    #number of existing user predictions for current week UCL
    UCL_predictions = MatchPrediction.objects.filter(user = request.user).filter(league__icontains= 'UEFA Champions League').filter(match_date__week=current_week).count()
    print(UCL_predictions, 'ucl games')
 
   


    if request.method == 'POST':
        pred = MatchPrediction.objects.filter(user=request.user).filter(matchApiId=pk).exists()
        print(pred)
        form = ApiMatchPredictionForm(request.POST)
        if form.is_valid():
            homeTeamScore = form.cleaned_data['homeTeamScore']
            awayTeamScore = form.cleaned_data['awayTeamScore']
            goalScorerName = form.cleaned_data['goalScorerName']
            #get player id from squad json object
            for player in squads:
                if player["name"] == goalScorerName:
                # If the name is found, print the associated id
                    goalScorerId = player["id"] 

            if pred == True:
                messages.error(request,'Prediction for this match alerady exists, please make prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            if match_datetime_object < timezone.now():
                messages.error(request,'Prediction match alredy started and can NOT be added on or edited. Please do prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            
            if match_league == 'UEFA Champions League':
                if UCL_predictions >= number_of_games_to_predict.UCL:
                    messages.error(request,f'You reach limit of {UCL_predictions} games to predict for UEFA Champions League already, delete your prediction to make new.')
                    return HttpResponseRedirect(request.path_info)
            
            if match_league != 'UEFA Champions League':
                if non_UCL_predictions >= number_of_games_to_predict.EPL:
                    messages.error(request,f'You reach limit of {non_UCL_predictions} games to predict already, delete your prediction to make new.')
                    return HttpResponseRedirect(request.path_info)
            

            print(form.cleaned_data)
            
            user = request.user.username
            u = User.objects.get(username=user)
            MatchPrediction.objects.create(
                matchApiId = pk,
                homeTeamScore=homeTeamScore,
                homeTeamName = hteam,
                awayTeamScore=awayTeamScore,
                awayTeamName = ateam,
                user = u,
                goalScorerName = goalScorerName,
                goalScorerId = goalScorerId,
                league = match_league,
                match_date = match_date
            )
            print('new prediction created')
            return redirect("predicts:predicts-home")


    context = {
        'match':match,
        'form':form,
        'hTeamSquad':hteam_squad,
        'hteam': hteam,
        'ateam': ateam,
        # 'key':key,
    }
    return render(request, 'match_prediction.html', context)

def match_prediction_update(request, pk):
    """Update view for match prediction"""
    pred = get_object_or_404(MatchPrediction, matchApiId=pk)

    hteam_squad = cache.get(f'{pred.homeTeamName}_squad')
    ateam_squad = cache.get(f'{pred.homeTeamName}_squad')
    squads = ateam_squad + hteam_squad
    # Create a list of choices from the dictionary
    choices = [(player['name'],player['name'] ) for player in squads]
   

    # Update the choices for the form field
    ApiMatchPredictionFormUpdat.base_fields['goalScorerName'].choices = choices



    if request.method == 'POST':
        form = ApiMatchPredictionFormUpdat(request.POST, instance=pred)
        if form.is_valid():
            form.save()
            return redirect('predicts:user_predictions')  # Replace 'success_page' with the desired URL name for the success page
    else:
        form = ApiMatchPredictionFormUpdat(instance=pred)

    context = {'form': form, 'hTeam':pred.homeTeamName, 'aTeam':pred.awayTeamName, 'match':pred.matchApiId, 'pred':pred}
    return render(request, 'match_prediction_update.html', context)




def delete_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(MatchPrediction, matchApiId = pk)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("predicts:user_predictions")
    
    context["prediction"] = obj
 
    return render(request, "prediction_delete.html", context)

def user_predictions_list(request, user):
    predictions = MatchPrediction.objects.filter(user__username = user).order_by('match_date')
    context = {
        'predictions': predictions
    }
       
    return render(request, 'user_predictions_list.html', context)

@staff_member_required
def single_match_update(request,pk):
    match = Match.objects.get(pk=pk)

    events_db = MatchEvents.objects.filter(match=pk)

    url = f'https://v3.football.api-sports.io/fixtures?id={match.match_id}'

    payload={}
    headers = {
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
        m = Match.objects.get(match_id=match.match_id)
        m.hTeamScore = int(hTeamScore)
        m.aTeamScore = int(aTeamScore)
        m.status = status
        m.save()
        print(f'match scores updated {m}')
    else:
        m = Match.objects.get(match_id=match.match_id)
        m.status = status
        m.date = response[0]['fixture']['date']
        #m.save()
        print('match not finished - date updated.')
    
    if events_db:
        print('events exist')
    else:
    
        #create events for match
        for event in events:
            match_id = match.match_id
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
                    #match_event.save()
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
                    #match_event.save()
                    print('Goal event created')
                else:
                    continue

            else:
                continue
        




    context={
        'response':response,
        'hTeamScore': hTeamScore,
        'aTeamScore':aTeamScore,
        'status':status,
        'events': events,
        'events_db':events_db,
        'match': match
    }
    return render(request,"single_match_update.html", context)

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