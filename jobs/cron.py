from django.utils import timezone
from predicts.models import  MatchPrediction, Match
import time
from datetime import date

def test_crone_job():
    now = timezone.now()
    # MatchEvents.objects.create(
    #     match_id = 123456789,
    #     team_id = 1,
    #     team_name = 'Test Team',
    #     time = 2,
    #     player_id = 12345,
    #     player_name = 'Test Player',
    #     type = 'test_event_type',
    #     detail = 'test_detail',
    # )
    print(now)
    
def auto_points_pending():
    print('\n AUTO POINTS START \n')
    today = date.today()
    matches = Match.objects.filter(finished=False).filter(date_date=today)
    for m in matches:
        m.update_match_data()
        m.save()
        time.sleep(2)

    print('\n AUTO POINTS END \n')

def auto_points_finish_today():
    print('\n AUTO POINTS START \n')
    today = date.today()
    matches = Match.objects.filter(finished=True).filter(date_date=today)
    for m in matches:
        m.update_match_data()
        m.save()
        print('match updated')
        time.sleep(2)

    print('\n AUTO POINTS END \n')

def points():
    today = timezone.now().date()
    print(today)
    unchecked_predictions = MatchPrediction.objects.filter(match__date__date=today)
    # unchecked_predictions = MatchPrediction.objects.filter(match__date_date=today)
    # print(unchecked_predictions)
    print(f'Start calculate points for unchecked {len(unchecked_predictions)} predictions')
    for prediction in unchecked_predictions:
        prediction.calculate_points()
        print(f'points calculated{prediction}')