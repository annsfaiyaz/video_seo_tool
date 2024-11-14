# FYP/video_seo_tool/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_seo_tool.settings')

app = Celery('video_seo_tool')

# Load task modules from all registered Django app video_seo_tool.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()