# services/youtube_service.py

import requests

API_KEY = "AIzaSyDf5BO-E5XZGq38D7iKlFxLa3rr09CM4i4"  # Replace with your actual API key

def get_categories(search_query):
    """
    Fetches video categories based on search parameters.
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "maxResults": 10,
        "q": search_query,
        "type": "video",
        "videoDuration": "any",
        "key": API_KEY
    }

    response = requests.get(search_url, params=search_params)
    if response.status_code == 200:
        search_data = response.json()
        video_ids = [item["id"]["videoId"] for item in search_data["items"]]
        return video_ids
    else:
        print("Failed to search videos:", response.status_code)
        return []

def get_videos_by_category(video_ids):
    """
    Fetches video details for a list of video IDs.
    """
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        "part": "snippet,statistics,status",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    response = requests.get(video_url, params=video_params)
    if response.status_code == 200:
        video_data = response.json().get("items", [])
        return video_data
    else:
        print("Failed to retrieve video details:", response.status_code)
        return []
