# your_app/youtube_service.py
import requests
from django.conf import settings

API_KEY = settings.YOUTUBE_API_KEY  # Ensure your API key is in your Django settings

BASE_URL = "https://www.googleapis.com/youtube/v3"

class YouTubeService:
    @staticmethod
    def fetch_popular_categories(region_code="PK"):
        """
        Fetches the most popular video categories for a given region.
        """
        url = f"{BASE_URL}/videoCategories"
        params = {
            "part": "snippet",
            "regionCode": region_code,
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        categories = response.json().get("items", [])
        return [{"id": item["id"], "title": item["snippet"]["title"]} for item in categories if item["snippet"]["assignable"]]

    @staticmethod
    def fetch_videos_by_category(category_id):
        """
        Fetches videos for a given category ID with all relevant data.
        """
        url = f"{BASE_URL}/search"
        params = {
            "part": "snippet",
            "type": "video",
            "videoCategoryId": category_id,
            "chart": "mostPopular",
            "maxResults": 2,  # Adjust the limit as needed
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        videos = response.json().get("items", [])
        video_details = []
        for video in videos:
            video_id = video["id"]["videoId"]
            # Fetch additional details for each video
            video_data = YouTubeService.fetch_video_details(video_id)
            video_details.append(video_data)
        return video_details

    @staticmethod
    def fetch_video_details(video_id):
        """
        Fetches detailed information for a specific video.
        """
        url = f"{BASE_URL}/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        video_info = response.json().get("items", [])
        if video_info:
            video_data = video_info[0]
            return {
                "videoId": video_data["id"],
                "title": video_data["snippet"]["title"],
                "description": video_data["snippet"]["description"],
                "channelId": video_data["snippet"]["channelId"],
                "publishedAt": video_data["snippet"]["publishedAt"],
                "likeCount": video_data["statistics"].get("likeCount"),
                "commentCount": video_data["statistics"].get("commentCount"),
                "viewCount": video_data["statistics"].get("viewCount"),
            }
        return None
