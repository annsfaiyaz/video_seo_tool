# app/tasks.py
from celery import shared_task
from app.services.youtube_service import YouTubeService

@shared_task
def fetch_youtube_data_task():
    
    categories = YouTubeService.fetch_popular_categories()
    for category in categories:
        if category.category_id == '19' or category.category_id == '27':
            continue  # I DID BECAUSE API HAVE SOME ISSUE ON 19
        YouTubeService.fetch_and_save_videos_by_category(category)
