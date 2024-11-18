import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Video

class TitleRecommender:
    def __init__(self):
        # Fetch and store all titles
        self.titles = list(Video.objects.values_list('title', flat=True))
        custom_stop_words = ['the', 'is', 'in', 'and', 'to', 'a']
        
        # Initialize and fit the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words=custom_stop_words)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.titles)
    
    def get_relevant_titles(self, new_title, top_k=5):
        # Transform the new title to a TF-IDF vector
        new_title_vec = self.vectorizer.transform([new_title])
        
        # Compute cosine similarity between the new title and all existing titles
        similarity_scores = cosine_similarity(new_title_vec, self.tfidf_matrix).flatten()
        
        # Get indices of the top K most similar titles
        top_indices = similarity_scores.argsort()[-top_k:][::-1]
        
        # Fetch the top K titles based on similarity
        relevant_titles = [self.titles[i] for i in top_indices]
        
        return relevant_titles
