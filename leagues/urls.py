from django.contrib import admin
from django.urls import path
from leagues.views import leagues_home


app_name = 'leagues'
urlpatterns = [
    path('', leagues_home, name='predicts-home'),

]
