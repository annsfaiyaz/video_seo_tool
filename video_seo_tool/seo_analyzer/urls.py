# # seo_analyzer/urls.py
# from django.urls import path
# from .views import index, suggestions, title_suggestions

# urlpatterns = [
#     path('', index, name='index'),  # This maps to the home page
#     path('suggestions/', suggestions, name='generate_suggestions'),  # This maps to the suggestions page
#     path('titles/<str:search_keyword>/', title_suggestions, name='title_suggestions'),  # This maps to title suggestions
# ]
from django.urls import path
from . import views
from .views import index, suggestions  # Ensure these functions are correctly imported

urlpatterns = [
    path('', index, name='index'),  # Home page
    path('suggestions/', suggestions, name='generate_suggestions'),  # Suggestions page
    path('youtube-data/', views.fetch_youtube_data, name='fetch_youtube_data'),

]