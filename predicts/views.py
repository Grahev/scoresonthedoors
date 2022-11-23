from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
import requests
import os
from .forms import MatchPredictionForm
from .models import Match, MatchPrediction, NumberOfGamesToPredict, Player, MatchEvents, Team
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from django.contrib import messages

#import for current week
from datetime import date
current_week = date.today().isocalendar()[1]  # return current week :)
# delete view import
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

#my functions import
from .my_functions import single_match_points



def predicts_home(request):
    # fixtures = Match.objects.all()

    fixtures = Match.objects.all() #all games
    #fixtures = Match.objects.filter(date__week=current_week) #query and display only current week games from monday to sunday
    # fixtures = Match.objects.filter(matchday='Regular Season - 1') #query and display only current week games from monday to sunday
    context={
        'fixtures':fixtures
    }
    return render(request, 'predicts_home.html', context)




def match_prediction(request):

    return render(request, 'prediction_create.html')


def user_predictions(request):
    """this view list all existings user predictions"""
    # user = User.objects.get(pk=pk)
    user = request.user

    user_predictions = MatchPrediction.objects.filter(user=user).order_by('-match__date')

    context = {
        'user':user,
        'user_predictions':user_predictions,

    }

    return render(request, 'user_predictions.html', context)


def match_prediction(request,pk):
    match = Match.objects.get(id=pk)
    form = MatchPredictionForm()
    md = match.matchday
    hteam = match.hTeam
    ateam = match.aTeam
    form = MatchPredictionForm(ht=hteam,at=ateam)
    m_id = match.match_id
    key = os.environ.get('key')
    number_of_games_to_predict = NumberOfGamesToPredict.objects.get(pk=1)
    print(f'\n number of EPL games to predict = {number_of_games_to_predict.EPL}')


    if request.method == 'POST':
        pred = MatchPrediction.objects.filter(user=request.user).filter(match__in=Match.objects.filter(id=pk)).exists()
        print(pred)
        print('post request')
        form = MatchPredictionForm(request.POST,ht=hteam,at=ateam)
        if form.is_valid():
            if pred == True:
                messages.error(request,'Prediction for this match alerady exists, please make prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            # if MatchPrediction.objects.filter(user = request.user).filter(match__in=Match.objects.filter(date__week=current_week)).count() >= 3:
            #     messages.error(request,'You predict 3 games already, delete your prediction to make new for this matchday.')
            #     return HttpResponseRedirect(request.path_info)
            if match.league == 'Premier League':
                if MatchPrediction.objects.filter(user = request.user).filter(match__league= 'Premier League').filter(match__in=Match.objects.filter(date__week=current_week)).count() >= number_of_games_to_predict.EPL:
                    messages.error(request,f'You predict {number_of_games_to_predict.EPL} games for Premier League already, delete your prediction to make new.')
                    return HttpResponseRedirect(request.path_info)
            if match.league != 'Premier League':
                if MatchPrediction.objects.filter(user = request.user).filter(match__league= 'UEFA Champions League').filter(match__in=Match.objects.filter(date__week=current_week)).count() >= number_of_games_to_predict.UCL:
                    messages.error(request,f'You predict {number_of_games_to_predict.UCL} game for Champions League already, delete your prediction to make new.')
                    return HttpResponseRedirect(request.path_info)
            if match.date < timezone.now():
                messages.error(request,'Prediction match alredy started and can NOT be added on or edited. Please do prediction for other match.')
                return HttpResponseRedirect(request.path_info)

            print(form.cleaned_data)
            homeTeamScore = form.cleaned_data['homeTeamScore']
            awayTeamScore = form.cleaned_data['awayTeamScore']
            goal = form.cleaned_data['goalScorer']
            user = request.user.username
            print(goal)
            u = User.objects.get(username=user)
            MatchPrediction.objects.create(
                match = match,
                homeTeamScore=homeTeamScore,
                awayTeamScore=awayTeamScore,
                user = u,
                goalScorer = goal,
            )
            print('new prediction created')
            return redirect("predicts:predicts-home")


    context = {
        'match':match,
        'form':form,
        'key':key,
    }
    return render(request, 'match_prediction.html', context)



def match_prediction_update(request, pk):
    """this is update view"""
    context ={}
    pred = MatchPrediction.objects.get(id=pk)
 
    # fetch the object related to passed id
    obj = get_object_or_404(MatchPrediction, id = pk)
    match = Match.objects.get(id=pred.match.id)
    hteam = match.hTeam
    ateam = match.aTeam
 
    # pass the object as instance in form
    form = MatchPredictionForm(request.POST or None, instance = obj,ht=hteam,at=ateam)
 
    # save the data from the form and
    # redirect
    if form.is_valid():
        form.save()
        return redirect("predicts:user_predictions")
 
    # add form dictionary to context
    context["form"] = form
    context["match"] = match
    context["prediction"] = pred
    return render(request, 'match_prediction_update.html', context)


def delete_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(MatchPrediction, id = pk)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("predicts:user_predictions")
    
    context["prediction"] = obj
 
    return render(request, "prediction_delete.html", context)

def user_predictions_list(request, user):
    predictions = MatchPrediction.objects.filter(user__username = user).order_by('-match__status','-match__date')
    context = {
        'predictions': predictions
    }
       
    return render(request, 'user_predictions_list.html', context)


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

def match_point_update(request, pk):
    """update points for all predictions for single match"""
    match = Match.objects.get(pk=pk)
    single_match_points(match)
    return render(request, 'single_match_points.html')