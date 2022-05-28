from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
import requests
import config
from .forms import MatchPredictionForm
from .models import Match



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