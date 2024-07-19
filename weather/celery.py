from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

# Create an instance of the Celery application with the name 'weather'.
app = Celery('weather')

# Configure the Celery application to use Django's settings.
# All Celery settings should start with the prefix 'CELERY_' in the Django settings file.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in the tasks.py modules of all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
