from celery import shared_task
from .views import generate_billing
from celery.schedules import crontab
from celery.task import periodic_task

@shared_task
def run_billing():
    generate_billing()
    return "Billing Process Completed"
    
@periodic_task(run_every=crontab(hour=0, minute=0)) 
def scheduled_billing():
    run_billing()