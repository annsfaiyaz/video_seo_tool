from django.shortcuts import render, redirect
from django.shortcuts import render
from .tasks import fetch_youtube_data_task
from app.ml_utils import TitleRecommender

def index(request):
    return render(request, 'app/index.html')


def suggestions(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', '')
        recommender = TitleRecommender()

        # Pass a new title and get relevant titles
        relevant_titles = recommender.get_relevant_titles(search_query, top_k=5)
        print("Relevant Titles:\n", relevant_titles)
        context = {
            'videos': relevant_titles,
            'search_query': search_query,
        }
        
        return render(request, 'app/suggestion_results.html', context)

    # If request method is not POST, redirect to index
    return redirect('index')

def fetch_youtube_data(request):
    
    # Trigger the Celery task
    fetch_youtube_data_task()
    # Redirect or return an immediate responsecategory
    return render(request, 'app/index.html', {"message": "Data fetching has started in the background."})
