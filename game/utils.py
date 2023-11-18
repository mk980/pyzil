from django.http import JsonResponse
import requests
from .models import Game, AnswersSet, TriviaQuestion, Question

from .models import CategoryList


def fetch_category_names():
	url = "https://opentdb.com/api_category.php"
	response = requests.get(url)

	if response.status_code == 200:
		data = response.json()
		categories = data.get("trivia_categories", [])

		for category in categories:
			category_id = category.get("id")
			name = category.get("name")

			# Check if the category exists in the database
			existing_category = CategoryList.objects.filter(category_id=category_id).first()

			# If the category doesn't exist, save it
			if not existing_category:
				category_instance = CategoryList(category_id=category_id, name=name)
				category_instance.save()

		return categories

	return []


def fetch_question():
	try:
		response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
		return response
	except Exception as e:
		print(f"Error fetching questions: {e}")
		return None


# def fetch_questions(difficulty_levels):
# 	for level in difficulty_levels:
# 		r = requests.get(f'https://opentdb.com/api.php?amount=3&difficulty={level}&type=multiple')
#
# 		game_data = json.loads(r.text).get('results')[0]
# 		save_game_data(game_data, level)


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
