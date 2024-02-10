from django.utils import timezone
from predicts.models import MatchEvents, MatchPrediction

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
    
def auto_points():
    print('\n AUTO POINTS START \n')
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

    print('\n AUTO POINTS END \n')

