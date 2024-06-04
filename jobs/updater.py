from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .cron import test_crone_job, auto_points_finish_today, auto_points_pending

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(test_crone_job, 'interval', minutes=1)
    scheduler.add_job(auto_points_finish_today, 'cron', hour=22, minute=57)
    scheduler.add_job(auto_points_pending, 'cron', minute='0,59', hour='17-23')
    scheduler.start()