from predicts.models import MatchPrediction
from leagues.models import League, WeeklyPoint, MonthlyPoint
import datetime
from django.contrib.auth.models import User

#get current week number
current_week = datetime.date.today().isocalendar()[1]

#get current year
current_year = datetime.date.today().year

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

    #get all predictions for league for current week and current year
    predictions = MatchPrediction.objects.filter(checked = False)
    for prediction in predictions:
        if prediction.checked == False and prediction.is_past_due:
            prediction.points = prediction.calculate_points()
            prediction.checked = True
            #update prediction points
            prediction.save()
           
            print(f'prediction: {prediction} - points: {prediction.points}')
        else:
            print(f'prediction: {prediction} is correct')

    #get all users
    # users = User.objects.all()

    # for user in users:
    #     user_predictions = MatchPrediction.objects.filter(user = user, checked = False, match_date__week = current_week, match_date__year = current_year)
    #     print(f'user: {user} len: {len(user_predictions)}')
    #     #check if user current week points exist if not create use get_or_create
    #     weekly_points, created = WeeklyPoint.objects.get_or_create(user = user, week_number = current_week, year = current_year)
    #     print(f'weekly_points: {weekly_points} created: {created}')

    #get all leagues
    leagues = League.objects.all()

    for league in leagues:
        league.weekly_points_calc()