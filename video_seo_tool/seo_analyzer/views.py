from django.shortcuts import render, redirect
import requests
from .services.youtube_service import get_categories, get_videos_by_category

def index(request):
    return render(request, 'seo_analyzer/index.html')


def suggestions(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', 'videos')

        # Step 1: Get video categories by search query
        video_ids = get_categories(search_query)

        # Step 2: Fetch video details using category IDs
        video_data = get_videos_by_category(video_ids)

        # Pass video data to the template
        context = {
            'search_query': search_query,
            'video_data': video_data,
        }
        return render(request, 'seo_analyzer/suggestion_results.html', context)

    # If request method is not POST, redirect to index
    return redirect('index')
