from django.shortcuts import render, redirect
from .services.youtube_service_sample import get_categories, get_videos_by_category
from django.shortcuts import render
from .services.youtube_service import YouTubeService
from app.models import Video
from django.db.models import Q
from .tasks import fetch_youtube_data_task

import pdb

def index(request):
    return render(request, 'app/index.html')


def suggestions(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', '')

        # Use Q objects to filter across multiple fields
        videos = Video.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct().order_by('-view_count', '-like_count')

        context = {
            'videos': videos,
            'search_query': search_query,
        }
        return render(request, 'app/suggestion_results.html', context)

    # If request method is not POST, redirect to index
    return redirect('index')

def fetch_youtube_data(request):
    
    # Trigger the Celery task
    fetch_youtube_data_task.delay()
    # Redirect or return an immediate responsecategory
    return render(request, 'app/index.html', {"message": "Data fetching has started in the background."})
