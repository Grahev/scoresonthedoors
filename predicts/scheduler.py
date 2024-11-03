# your_app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from datetime import timedelta
from .models import Match, MatchPrediction

def update_matches_and_calculate_points():
    today = timezone.now().date()
    matches = Match.objects.filter(date__date=today)
    
    for match in matches:
        match.update_match_data()
        
        predictions = MatchPrediction.objects.filter(match=match)
        for prediction in predictions:
            prediction.calculate_points()

def update_matches():
    # Get the current date and time
    now = timezone.now()
    
    # Calculate the date 3 days ago
    three_days_ago = now - timedelta(days=2)

    # Get only the date part
    start_date = three_days_ago.date()
    end_date = now.date()
    
    matches = Match.objects.filter(date__date__range=[start_date, end_date])
    print(f'matches to update: {len(matches)} \n START UPDATE')

    for match in matches:
        match.update_match_data()
        if match.finished:
            match.finished_match_data_save()

    print('END UPDATE')

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Schedule job to run every 30 minutes between 14:00 and 23:00
scheduler.add_job(
    update_matches_and_calculate_points,
    'cron',
    minute='0,30',
    hour='13-23',
    id='update_matches_and_calculate_points',
    replace_existing=True
)

scheduler.add_job(
    update_matches,
    'cron',
    minute='0,30',
    hour='13-22',
    id='update_matches_from_today_and_older',
    replace_existing=True
)

register_events(scheduler)
scheduler.start()

print("Scheduler started...")
