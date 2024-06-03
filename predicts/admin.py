from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import MatchPrediction, Match, NumberOfGamesToPredict, LiveLeague

class MatchAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'match_id', 'hTeam_name', 'aTeam_name', 'date', 'started', 'finished', 
        'hTeamScore', 'aTeamScore', 'league', 'league_sezon'
    )
    
    # Fields to search
    search_fields = (
        'hTeam_name', 'aTeam_name', 'league', 'league_sezon'
    )
    
    # Fields to filter
    list_filter = (
        'started', 'finished', 'league', 'league_sezon', 'date'
    )
    
    # Optionally, you can add ordering
    ordering = ('-date',)
    
    # Add a custom action to update match data
    actions = ['update_match_data']

    def update_match_data(self, request, queryset):
        for match in queryset:
            match.update_match_data()
        self.message_user(request, "Match data updated successfully.")
    update_match_data.short_description = "Update Match Data"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:match_id>/update/', self.admin_site.admin_view(self.update_single_match), name='update_match_data'),
        ]
        return custom_urls + urls

    def update_single_match(self, request, match_id):
        match = get_object_or_404(Match, pk=match_id)
        match.update_match_data()
        self.message_user(request, "Match data updated successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['update_match_data_url'] = f'{object_id}/update/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

class MatchPredictionAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'user', 'match', 'homeTeamScore', 'awayTeamScore', 'goalScorerName', 
        'checked', 'points', 'onextwo'
    )
    
    # Fields to search
    search_fields = (
        'user__username', 'goalScorerName', 'match__hTeam_name', 'match__aTeam_name', 'onextwo'
    )
    
    # Fields to filter
    list_filter = (
        'checked', 'points', 'onextwo', 'match'
    )
    
    # Optionally, you can add ordering
    ordering = ('-match__date', 'user')

admin.site.register(Match, MatchAdmin)
admin.site.register(MatchPrediction, MatchPredictionAdmin)
admin.site.register(NumberOfGamesToPredict)
admin.site.register(LiveLeague)

# from django.contrib import admin
# from .models import MatchPrediction, Match, NumberOfGamesToPredict, LiveLeague

# # Register your models here.

# class MatchAdmin(admin.ModelAdmin):
#     # Fields to display in the list view
#     list_display = (
#         'match_id', 'hTeam_name', 'aTeam_name', 'date', 'started', 'finished', 
#         'hTeamScore', 'aTeamScore', 'league', 'league_sezon'
#     )
    
#     # Fields to search
#     search_fields = (
#         'hTeam_name', 'aTeam_name', 'league', 'league_sezon'
#     )
    
#     # Fields to filter
#     list_filter = (
#         'started', 'finished', 'league', 'league_sezon', 'date'
#     )
    
#     # Optionally, you can add ordering
#     ordering = ('-date',)

# class MatchPredictionAdmin(admin.ModelAdmin):
#     # Fields to display in the list view
#     list_display = (
#         'user', 'match', 'homeTeamScore', 'awayTeamScore', 'goalScorerName', 
#         'checked', 'points', 'onextwo'
#     )
    
#     # Fields to search
#     search_fields = (
#         'user__username', 'goalScorerName', 'match__hTeam_name', 'match__aTeam_name', 'onextwo'
#     )
    
#     # Fields to filter
#     list_filter = (
#         'checked', 'points', 'onextwo', 'match'
#     )
    
#     # Optionally, you can add ordering
#     ordering = ('-match__date', 'user')

# admin.site.register(Match, MatchAdmin)
# admin.site.register(MatchPrediction, MatchPredictionAdmin)
# admin.site.register(NumberOfGamesToPredict),
# admin.site.register(LiveLeague),
