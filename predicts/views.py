from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
import requests
import config
from .forms import MatchPredictionForm
from .models import Match, MatchPrediction
from django.contrib.auth.models import User



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
    user = User.objects.get(pk=pk)

    user_predictions = MatchPrediction.objects.filter(user=user)

    context = {
        'user':user,
        'user_predictions':user_predictions,

    }

    return render(request, 'user_predictions.html', context)