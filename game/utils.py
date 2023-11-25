from django.http import JsonResponse
import requests
from .models import GameSession, AnswersSet, TriviaQuestion


def fetch_question():
    try:
        response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
        return response  # Return the response object directly
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return None




