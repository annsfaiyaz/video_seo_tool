# app/tasks.py
from celery import shared_task
from app.services.youtube_service import YouTubeService

@shared_task
def fetch_youtube_data_task():
    
    categories = YouTubeService.fetch_popular_categories()
    for category in categories:
        YouTubeService.fetch_and_save_videos_by_category(category)
