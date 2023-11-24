import logging
from django.shortcuts import redirect, render
from .utils import fetch_question
from django.contrib import messages
from .models import AnswersSet, TriviaQuestion
logging.basicConfig(level=logging.DEBUG)


def index(request):
    return render(request, 'game/index.html')


def calculate_progress_color(progress_ratio):
    if progress_ratio < 25:
        return 'bg-danger'
    elif progress_ratio < 50:
        return 'bg-warning'
    elif progress_ratio < 75:
        return 'bg-info'
    else:
        return 'bg-success'


def game_view(request):
    logging.debug("Entered game_view function")
    logging.debug(request.session.items())
    log_items = {key: value for key, value in request.session.items() if key != 'asked_questions'}
    logging.debug(log_items)

    if not request.session:
        request.session.clear()
        request.session.modified = True
        # Reset relevant session variables to their initial values
        request.session['question_counter'] = 0
        request.session['attempts'] = 0
        request.session['initialized'] = True

    current_question_id = request.session.get('current_question')

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
            question = get_current_question(request)

            render(request,
                   'game/game_screen.html',
                   {'question': question, 'current_question_id': current_question_id})

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
                request.session['current_question'] = question.pk
    question_counter = request.session.get('question_counter', 0)
    attempts = request.session.get('attempts', 0)
    total_questions = 10  # Total question in the game
    progress_ratio = (request.session.get('question_counter', 0) / total_questions) * 100
    progress_color = calculate_progress_color(progress_ratio)
    current_question_id = request.session.get('current_question')

    logging.debug(f"Question counter: {question_counter}")
    logging.debug(f"Attempts: {attempts}")
    logging.debug(f"Current question ID: {current_question_id}")
    logging.debug(f"Progress ratio: {progress_ratio}")

    question = TriviaQuestion.objects.order_by('?').first()
    return render(request,
                  'game/game_screen.html',
                  {'question': question,
                   'progress_ratio': progress_ratio,
                   'progress_color': progress_color,
                   'current_question_id': current_question_id})


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

    try:
        current_question = TriviaQuestion.objects.get(pk=current_question_id)
    except TriviaQuestion.DoesNotExist:
        current_question = None
    return current_question


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
