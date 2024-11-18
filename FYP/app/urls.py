
from django.urls import path
from . import views
from .views import index, suggestions  # Ensure these functions are correctly imported

urlpatterns = [
    path('', index, name='index'),  # Home page
    path('suggestions/', suggestions, name='generate_suggestions'),  # Suggestions page
    path('youtube-data/', views.fetch_youtube_data, name='fetch_youtube_data'),
]