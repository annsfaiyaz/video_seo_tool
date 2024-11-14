# your_app/youtube_service.py
import requests
from django.conf import settings
from app.models import Category, Video, Channel, Tag
from django.utils.dateparse import parse_datetime
import pdb

API_KEY = settings.YOUTUBE_API_KEY  # Ensure your API key is in your Django settings
BASE_URL = "https://www.googleapis.com/youtube/v3"

class YouTubeService:
    
    @staticmethod
    def fetch_popular_categories(region_code="PK"):
        url = f"{BASE_URL}/videoCategories"
        params = {
            "part": "snippet",
            "regionCode": region_code,
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        categories = response.json().get("items", [])

        saved_categories = []
        for item in categories:
            if item["snippet"]["assignable"]:
                title = item["snippet"]["title"]
                channel_id =  item['snippet']['channelId']
                category_id = item["id"]
                # Save or update category in the database
                category, created = Category.objects.update_or_create(
                    title=title,
                    defaults={"channel_id": channel_id, "category_id": category_id, "region": region_code}
                )
                saved_categories.append(category)

        return saved_categories

    # @staticmethodYouTubeService
    # def fetch_videos_by_category(category):
    #     """
    #     Fetches videos for a given category ID with all relevant data.
    #     """
    #     url = f"{BASE_URL}/search"
    #     params = {
    #         "part": "snippet",
    #         "type": "video",
    #         "videoCategoryId": category_id,
    #         "chart": "mostPopular",
    #         "maxResults": 2,  # Adjust the limit as needed
    #         "key": API_KEY
    #     }
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     videos = response.json().get("items", [])
    #     video_details = []
    #     for video in videos:
    #         video_id = video["id"]["videoId"]
    #         # Fetch additional details for each video
    #         video_data = YouTubeService.fetch_video_details(video_id)
    #         video_details.append(video_data)
    #     return video_details

    @staticmethod
    # def fetch_video_details(video_id):
    #     """
    #     Fetches detailed information for a specific video.
    #     """
    #     url = f"{BASE_URL}/videos"
    #     params = {
    #         "part": "snippet,statistics",
    #         "id": video_id,
    #         "key": API_KEY
    #     }
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     video_info = response.json().get("items", [])
    #     if video_info:
    #         video_data = video_info[0]
    #         return {
    #             "videoId": video_data["id"],
    #             "title": video_data["snippet"]["title"],
    #             "description": video_data["snippet"]["description"],
    #             "channelId": video_data["snippet"]["channelId"],
    #             "publishedAt": video_data["snippet"]["publishedAt"],
    #             "likeCount": video_data["statistics"].get("likeCount"),
    #             "commentCount": video_data["statistics"].get("commentCount"),
    #             "viewCount": video_data["statistics"].get("viewCount"),
    #         }
    #     return None
    
    @staticmethod
    def fetch_and_save_videos_by_category(saved_category):
        # Fetch videos from YouTube API
        url = f"{BASE_URL}/videos"
        params = {
            "part": "snippet, statistics",
            "chart": "mostPopular",
            "videoCategoryId": saved_category.category_id,
            "regionCode": "PK",
            "key": API_KEY
        }
        # pdb.set_trace()
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        videos = response.json().get("items", [])

        for video_data in videos:
            snippet = video_data["snippet"]
            statistics = video_data.get("statistics", {})

            # Get or create channel
            channel, _ = Channel.objects.get_or_create(
                channel_id=snippet["channelId"],
                defaults={"name": snippet.get("channelTitle", "Unknown Channel")}
            )

            # Get or create category
            category, _ = Category.objects.get_or_create(
                category_id=snippet.get("categoryId"),
                defaults={"title": snippet.get("title", "No title")}
            )
            
            print(snippet.get("title", "No title"))
            # Get or create video
            
            video, created = Video.objects.update_or_create(
                video_id=video_data["id"],
                defaults={
                    "category": category,
                    "channel": channel,
                    "title": snippet.get("title", "No title"),
                    "description": snippet.get("description", ""),
                    "published_at": parse_datetime(snippet["publishedAt"]),
                    "like_count": int(statistics.get("likeCount", 0)),
                    "comment_count": int(statistics.get("commentCount", 0)),
                    "view_count": int(statistics.get("viewCount", 0)),
                }
            )

            # Handle tags
            tags = snippet.get("tags", [])
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                video.tags.add(tag)