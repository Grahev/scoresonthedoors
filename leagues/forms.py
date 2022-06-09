from django import forms
from crispy_forms.helper import FormHelper

from leagues.models import League


class LeagueCreateModelForm(forms.ModelForm):
    class Meta:
        model = League
        fields = [
            'name',
            'pin',
            'rules'
        ]

    def __init__(self, *args, **kwargs):
        super(LeagueCreateModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True 
        self.fields['name'].label = 'League Name'
        self.fields['pin'].label = 'League PIN'
        self.fields['rules'].help_text = "Enter your league rules / notes / info etc. This will be display in bottom of your league table and be visible for all league members."
        self.fields['pin'].help_text = 'Pin will be used to verify new members.'


class JoinLeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = ['name', 'pin']

class LeagueJoinPinForm(forms.Form):
    pin = forms.IntegerField()