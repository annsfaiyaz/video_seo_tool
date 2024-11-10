from django.shortcuts import render, redirect
from .services.youtube_service_sample import get_categories, get_videos_by_category
from django.shortcuts import render
from .services.youtube_service import YouTubeService
from seo_analyzer.models import Video
from django.db.models import Q

import pdb

def index(request):
    return render(request, 'seo_analyzer/index.html')


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
        return render(request, 'seo_analyzer/suggestion_results.html', context)

    # If request method is not POST, redirect to index
    return redirect('index')

def fetch_youtube_data(request):
    categories = YouTubeService.fetch_popular_categories()
    # pdb.set_trace()
    for category in categories:
        YouTubeService.fetch_and_save_videos_by_category(category)
    return render(request, 'seo_analyzer/index.html')