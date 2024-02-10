from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .cron import test_crone_job, auto_points

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(test_crone_job, 'interval', minutes=1)
    scheduler.add_job(auto_points, 'cron', hour=22, minute=30)
    scheduler.start()