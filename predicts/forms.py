from attr import field
from django import forms  
from .models import MatchPrediction
from django.contrib.auth.models import User
from teams_and_players.models import Player

#crispy form import
from crispy_forms.helper import FormHelper


class MatchPredictionForm(forms.ModelForm):

    class Meta:
        model = MatchPrediction
        fields = ['homeTeamScore','awayTeamScore','goalScorer']

    def __init__(self, *args, **kwargs):
        ht = kwargs.pop('ht',None)
        at = kwargs.pop('at',None)
        super(MatchPredictionForm,self).__init__(*args, **kwargs)
        self.fields['goalScorer'].queryset= Player.objects.filter(team__in=[ht,at])
        self.fields['homeTeamScore'].label = ht
        self.fields['awayTeamScore'].label = at
        self.helper = FormHelper()
        self.helper.form_show_labels = False