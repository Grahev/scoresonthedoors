from django.contrib import admin
from .models import MatchPrediction, Match, MatchEvents

# Register your models here.

admin.site.register(MatchPrediction),
admin.site.register(Match),
admin.site.register(MatchEvents),
