from django.shortcuts import render, redirect
from .services.youtube_service_sample import get_categories, get_videos_by_category
# from .services.youtube_service_sample import fetch_and_save_latest_videos
# your_app/views.py
from django.shortcuts import render
from .services.youtube_service import YouTubeService

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

def fetch_youtube_data(request):
    categories = YouTubeService.fetch_popular_categories()
    videos_data = []
    for category in categories:
        videos = YouTubeService.fetch_videos_by_category(category["id"])
        videos_data.append({"category": category["title"], "videos": videos})
    return render(request, "seo_analyzer/youtube_data.html", {"categories": categories, "videos_data": videos_data})

# def fetch_latest_youtube_data(request):
    if request.method == "POST":
        fetch_and_save_latest_videos()  # Fetch and save latest videos
        return redirect('index')  # Redirect to the homepage or any page you prefer