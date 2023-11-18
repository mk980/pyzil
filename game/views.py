from django.shortcuts import redirect, render
from .utils import fetch_question

from .models import AnswersSet, TriviaQuestion


def index(request):
	return render(request, 'game/index.html')


def game_view(request):
	if request.method == 'POST':
		# Handle answer submission
		selected_answer = request.POST.get('answer')
		correct_answer = TriviaQuestion.objects.get(pk=request.POST.get('question_id')).answer_set.correct_answer

		# Determine if the selected answer is correct and handle accordingly
		is_correct = selected_answer == correct_answer
		context = {'is_correct': is_correct}
		return render(request, 'game/game_screen.html', context)

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

	question = TriviaQuestion.objects.order_by('?').first()
	return render(request, 'game/game_screen.html', {'question': question})
# return render(request, 'game/game_screen.html', {'get_question': get_question})
