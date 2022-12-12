from attr import field
from django import forms  
from .models import MatchPrediction
from django.contrib.auth.models import User
from teams_and_players.models import Player

#crispy form import
from crispy_forms.helper import FormHelper


# class ApiMatchPredictionForm(forms.Form):
    
#     homeTeamName = forms.CharField()
#     homeTeamId = forms.IntegerField()
#     homeTeamScore = forms.IntegerField(min_value=0, max_value=10)
    
#     awayTeamName = forms.CharField()
#     awayTeamId = forms.IntegerField()
#     awayTeamScore = forms.IntegerField(min_value=0, max_value=10)

#     goalScorer = forms.ChoiceField(choices=[])
#     goalScorerId = forms.IntegerField()


class ApiMatchPredictionForm(forms.ModelForm):

    goalScorerName = forms.ChoiceField(choices=[])
    homeTeamScore = forms.IntegerField(initial=0)
    awayTeamScore = forms.IntegerField(initial=0)

    class Meta:
        model = MatchPrediction
        fields  = ['homeTeamScore','awayTeamScore','goalScorerName']
        labels = {}
