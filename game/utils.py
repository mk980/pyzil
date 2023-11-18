from django.http import JsonResponse
import requests
from .models import Game, AnswersSet, TriviaQuestion


def fetch_question():
	try:
		response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
		return response
	except Exception as e:
		print(f"Error fetching questions: {e}")
		return None


def save_game_data(game_data, difficulty_level):
	correct_answer = game_data.get('correct_answer')
	incorrect_answers = game_data.get('incorrect_answers')
	incorrect_answer1 = incorrect_answers[0]
	incorrect_answer2 = incorrect_answers[1]
	incorrect_answer3 = incorrect_answers[2]
	answers_set = AnswersSet(
		correct_answer=correct_answer,
		incorrect_answer1=incorrect_answer1,
		incorrect_answer2=incorrect_answer2,
		incorrect_answer3=incorrect_answer3,
	)
	answers_set.save()
	question = Question(
		answer_set=answers_set,
		difficulty_level=difficulty_level,
	)
	question.save()
	new_game = Game(
		question=question
	)
	new_game.save()





def calculate_score(question_difficulty, is_correct=False):
	pass
