import requests


def fetch_question():
    try:
        response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
        return response
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return None




