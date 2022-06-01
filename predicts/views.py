from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
import requests
import config
from .forms import MatchPredictionForm
from .models import Match, MatchPrediction
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
from django.contrib import messages



def predicts_home(request):
    fixtures = Match.objects.all()
    context={
        'fixtures':fixtures
    }
    return render(request, 'predicts_home.html', context)


def predicts_list(request,league,year):
    
    return render(request,'test.html')


def match_prediction(request):

    return render(request, 'prediction_create.html')


def user_predictions(request,pk):
    """this view list all existings user predictions"""
    user = User.objects.get(pk=pk)

    user_predictions = MatchPrediction.objects.filter(user=user)

    context = {
        'user':user,
        'user_predictions':user_predictions,

    }

    return render(request, 'user_predictions.html', context)

#//TODO add create prediction view

def match_prediction(request,pk):
    match = Match.objects.get(id=pk)
    form = MatchPredictionForm()
    md = match.matchday
    hteam = match.hTeam
    ateam = match.aTeam
    form = MatchPredictionForm(ht=hteam,at=ateam)
    m_id = match.match_id
    key = config.key
    # key = os.environ.get('key')
    print(m_id)


    print(match.date)
    print(timezone.now())
    if match.date < timezone.now():
        print('matchday is smaller')
    else:
        print('time now is bigger')


    if request.method == 'POST':
        pred = MatchPrediction.objects.filter(user=request.user).filter(match__in=Match.objects.filter(id=pk)).exists()
        print(pred)
        print('post request')
        form = MatchPredictionForm(request.POST,ht=hteam,at=ateam)
        if form.is_valid():
            if pred == True:
                messages.error(request,'Prediction for this match alerady exists, please make prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            if MatchPrediction.objects.filter(user = request.user).filter(match__in=Match.objects.filter(matchday=md)).count() >= 3:
                print('if statment')
                # print(MatchPrediction.objects.filter(user = request.user).filter(match__in=Match.objects.filter(matchday=md)).count())
                messages.error(request,'You predict 3 games already, delete your prediction to make new for this matchday.')
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


#//TODO create match_prediction edid view