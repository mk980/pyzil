import logging
from django.shortcuts import redirect, render
from .utils import fetch_question
from django.contrib import messages
from .models import AnswersSet, TriviaQuestion
logging.basicConfig(level=logging.DEBUG)


def index(request):
    return render(request, 'game/index.html')


def game_view(request):
    logging.debug("Entered game_view function")
    logging.debug(request.session.items())
    log_items = {key: value for key, value in request.session.items() if key != 'asked_questions'}
    logging.debug(log_items)


    # if request.method == 'POST':
        # request.session['question_counter'] = 1
    if 'new_session' in request.GET:
        request.session.flush()

    if request.method == 'POST':
        logging.debug("Received POST request")

        question_id = request.POST.get('question')
        user_answer = request.POST.get('option')
        correct_answer = request.POST.get('answer_label')

        if user_answer == correct_answer:
            question_counter = request.session.get('question_counter', 0)
            request.session['question_counter'] = question_counter + 1
            request.session['attempts'] = 0
            messages.success(request, 'Correct answer')
            return handle_next_question(request)
        else:
            attempts = request.session.get('attempts', 0)
            request.session['attempts'] = attempts + 1

            if attempts >= 2:
                messages.warning(request, f'Wrong answer, Correct Answer is {correct_answer}')

            messages.warning(request, f'Wrong answer, try again. Attempts remaining: {(2 - attempts)}')

            request.session.get('current_question_id')
            question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3 = get_current_question(request) # noqa
            return render(request,
                          'game/game_screen.html',
                          {'question': question,
                           'correct_answer': correct_answer,
                           'incorrect_answer1': incorrect_answer1,
                           'incorrect_answer2': incorrect_answer2,
                           'incorrect_answer3': incorrect_answer3})

    response = fetch_question()
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if results:
            for result in results:
                incorrect_answers = result.get("incorrect_answers")
                answers_set = AnswersSet(
                    correct_answer=result.get("correct_answer"),
                    incorrect_answer1=incorrect_answers[0],
                    incorrect_answer2=incorrect_answers[1],
                    incorrect_answer3=incorrect_answers[2]
                )
                answers_set.save()

                question = TriviaQuestion(
                    category=result.get("category"),
                    difficulty=result.get("difficulty"),
                    question=result.get("question"),
                    type=result.get("type"),
                    answer_set=answers_set
                )
                question.save()

    question_counter = request.session.get('question_counter', 0)
    attempts = request.session.get('attempts', 0)
    current_question_id = request.session.get('current_question')

    logging.debug(f"Question counter: {question_counter}")
    logging.debug(f"Attempts: {attempts}")
    logging.debug(f"Current question ID: {current_question_id}")

    question = TriviaQuestion.objects.order_by('?').first()
    return render(request, 'game/game_screen.html', {'question': question})


def handle_next_question(request):
    # Update current_question_id to the ID of the next question
    next_question_id = get_next_question(request)
    if next_question_id is not None:
        request.session['current_question'] = next_question_id
    question_counter = request.session.get('question_counter', 0)
    # request.session['question_counter'] = question_counter + 1
    request.session['attempts'] = 0
    if question_counter >= 10:
        return render(request, 'game/game_finished.html')

    return redirect('game_view')


def get_current_question(request):
    current_question_id = request.session.get('current_question')
    current_question = None
    correct_answer = None
    incorrect_answer1 = None
    incorrect_answer2 = None
    incorrect_answer3 = None
    try:
        current_question_object = TriviaQuestion.objects.get(pk=current_question_id)
        current_question = current_question_object.question
        correct_answer = current_question_object.answer_set.correct_answer
        incorrect_answer1 = current_question_object.answer_set.incorrect_answer1
        incorrect_answer2 = current_question_object.answer_set.incorrect_answer2
        incorrect_answer3 = current_question_object.answer_set.incorrect_answer3

    except TriviaQuestion.DoesNotExist:
        current_question = None

    return current_question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3


def get_next_question(request):

    request.session.setdefault('asked_questions', [])

    asked_question_ids = request.session['asked_questions']
    next_question = TriviaQuestion.objects.order_by('?').exclude(
        pk__in=asked_question_ids
    ).first()

    if next_question:
        next_question_id = next_question.pk
        # Append the ID of the next question to the asked_questions session variable
        request.session['asked_questions'].append(next_question_id)
    else:
        next_question_id = None

    return next_question_id
