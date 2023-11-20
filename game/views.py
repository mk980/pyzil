from django.shortcuts import redirect, render
from .utils import fetch_question
from django.contrib import messages
from .models import AnswersSet, TriviaQuestion


def index(request):
	return render(request, 'game/index.html')


def game_view(request):
	if request.method == 'POST':
		# Handle answer submission
		question_id = request.POST.get('question')
		user_answer = request.POST.get('option')
		correct_answer = request.POST.get('answer_label')

		if user_answer == correct_answer:
			messages.success(request, 'Correct answer')
			handle_correct_answer(request, question_id)
		else:
			handle_incorrect_answer(request, correct_answer)

	question = get_current_question(request)

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


def handle_correct_answer(request, question_id):
	# Increment the session's question counter
	question_counter = request.session.get('question_counter', 0)
	request.session['question_counter'] = question_counter + 1

	if question_counter >= 10:  # Max questions for the game
		# Game finished, redirect to a completion page or take other actions
		return render(request, 'game/game_finished.html')

	# Move to the next question
	next_question_id = get_next_question(request)

	# Set the current question in the session
	request.session['current_question'] = next_question_id
	# Reset attempts for the new question
	request.session['attempts'] = 0


def handle_incorrect_answer(request, correct_answer):
	attempts = request.session.get('attempts', 0)
	request.session['attempts'] = attempts + 1

	if attempts >= 2:  # User has no further attempts left
		messages.warning(request, f'Wrong answer, Correct Answer is {correct_answer}')
		return render(request, 'game/no_more_questions.html')

	messages.warning(request, f'Wrong answer, try again. Attempts remaining: {2 - attempts}')


def get_current_question(request):
	current_question_id = request.session.get('current_question')
	try:
		current_question = TriviaQuestion.objects.get(pk=current_question_id)
	except TriviaQuestion.DoesNotExist:
		current_question = None

	return current_question


def get_next_question(request):
	# Try to get the next question
	asked_question_ids = request.session.get('asked_questions', [])
	next_question = TriviaQuestion.objects.order_by('?').exclude(
		pk__in=asked_question_ids
	).first()

	if next_question:
		next_question_id = next_question.pk
		# Append the ID of the next question to the asked_questions session variable
		request.session.setdefault('asked_questions', []).append(next_question_id)
	else:
		next_question_id = None

	return next_question_id
