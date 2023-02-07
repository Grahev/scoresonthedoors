from django.contrib import admin
from .models import MatchPrediction, Match, MatchEvents, NumberOfGamesToPredict

# Register your models here.



class MatchPredictionAdmin(admin.ModelAdmin):
    list_display = ('match', 'user', 'homeTeamScore', 'awayTeamScore', 'points')
    list_filter = ('match', 'user', 'homeTeamScore', 'awayTeamScore', 'points')
    search_fields = ('match', 'user', 'homeTeamScore', 'awayTeamScore', 'points')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('hTeam', 'aTeam', 'date', 'matchday', 'status', 'match_id')
    list_filter = ('hTeam', 'aTeam', 'date', 'matchday', 'status', 'match_id')
    search_fields = ('hTeam', 'aTeam', 'date', 'matchday', 'status', 'match_id')


admin.site.register(MatchPrediction, MatchPredictionAdmin),
admin.site.register(Match, MatchAdmin),
admin.site.register(MatchEvents),
admin.site.register(NumberOfGamesToPredict),