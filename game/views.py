from django.shortcuts import redirect, render

from .utils import fetch_question

from .models import AnswersSet, TriviaQuestion


def index(request):
	return render(request, 'game/index.html')


def game_view(request):
	# get_question = TriviaQuestion.objects.all()
	# get_answer = AnswersSet.objects.all()
	response = fetch_question()
	if response.status_code == 200:
		data = response.json()
		results = data.get("results", {"results": "No results"})

		if results:
			for result in results:
				incorrect_answers = result.get("incorrect_answers")
				# AnswerSet instance for Associated TriviaQuestion

				answers_set = AnswersSet(
					correct_answer=result.get("correct_answer"),
					incorrect_answer1=incorrect_answers[0],
					incorrect_answer2=incorrect_answers[1],
					incorrect_answer3=incorrect_answers[2]
				)
				answers_set.save()
				# TriviaQuestion instance
				question = TriviaQuestion(
					category=result.get("category"),
					difficulty=result.get("difficulty"),
					question=result.get("question"),
					type=result.get("type"),
					answer_set=answers_set

				)
				question.save()

	question = TriviaQuestion.objects.all()
	return render(request, 'game/game_screen.html', {'question': question})
# return render(request, 'game/game_screen.html', {'get_question': get_question})
