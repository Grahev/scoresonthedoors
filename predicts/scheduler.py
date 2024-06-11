# your_app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from .models import Match, MatchPrediction

def update_matches_and_calculate_points():
    today = timezone.now().date()
    matches = Match.objects.filter(date__date=today)
    
    for match in matches:
        match.update_match_data()
        
        predictions = MatchPrediction.objects.filter(match=match)
        for prediction in predictions:
            prediction.calculate_points()

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

register_events(scheduler)
scheduler.start()

print("Scheduler started...")
