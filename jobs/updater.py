from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .cron import test_crone_job, auto_points_finish_today, auto_points_pending, points

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(test_crone_job, 'interval', minutes=1)
    # scheduler.add_job(auto_points_finish_today, 'cron', hour=22, minute=47)
    scheduler.add_job(auto_points_pending, 'cron', minute="*")
    # scheduler.add_job(auto_points_pending, 'cron', minute='0,59', hour='14-23')
    # scheduler.add_job(points, 'cron', minute='*/10', hour='14-23')
    scheduler.start()