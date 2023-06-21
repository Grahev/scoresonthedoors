from predicts.models import MatchPrediction
from leagues.models import League, WeeklyPoint, MonthlyPoint
import datetime
from django.contrib.auth.models import User



#

points_dict = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

def run():
    #get current week number
    current_week = datetime.date.today().isocalendar()[1]

    #get current year
    current_year = datetime.date.today().year



    #get all leagues
    leagues = League.objects.all()

    for league in leagues:
        league.monthly_points_calc()


    


