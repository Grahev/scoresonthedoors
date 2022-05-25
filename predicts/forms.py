from attr import field
from django import forms  
from .models import MatchPrediction
from django.contrib.auth.models import User


class MatchPredictionForm(forms.ModelForm):

    class Meta:
        model = MatchPrediction
        fields = '__all__'
        