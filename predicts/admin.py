from django.contrib import admin
from .models import MatchPrediction, Match, MatchEvents, NumberOfGamesToPredict, MatchResult, LiveLeague

# Register your models here.

admin.site.register(MatchPrediction),
admin.site.register(Match),
admin.site.register(MatchEvents),
admin.site.register(NumberOfGamesToPredict),
admin.site.register(MatchResult),
admin.site.register(LiveLeague),
