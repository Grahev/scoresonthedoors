from django.contrib import admin
from .models import MatchPrediction, Match

# Register your models here.

admin.site.register(MatchPrediction),
admin.site.register(Match),
