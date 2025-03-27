import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bright_credit.settings")

app = Celery("bright_credit")

# Load Celery config from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()
