from django.contrib import admin
from django.urls import path
from leagues.views import maximum_leagues,league_delete, leagues_home, LeagueCreateView,LeaguesListView, leave_league, league_details, leave_league_confirm, join_league,join_league_pin, league_old_points, user_statistics


app_name = 'leagues'
urlpatterns = [
    path('', LeaguesListView.as_view(), name='leagues-home'),
    path('create/', LeagueCreateView.as_view(), name='league-create'),
    path('<int:pk>/',league_details, name='league_details'),
    path('leave/<int:pk>', leave_league, name='leave-league'),
    path('leave/confirm/<int:pk>', leave_league_confirm, name='leave-league_confirm'),
    path('join/', join_league, name='join-league'),
    path('join/<int:pk>/', join_league_pin, name='join_league'),
    path('maximum_leagues/', maximum_leagues, name='maximum-leagues'),
    path('<int:pk>/delete', league_delete, name='league-delete'),
    path('old/', league_old_points, name='league-old-points'),
    path('statistics/<int:pk>', user_statistics, name='user-statistics'),

]
