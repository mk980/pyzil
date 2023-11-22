import logging
from django.shortcuts import redirect, render
from .utils import fetch_question
from django.contrib import messages
from .models import AnswersSet, TriviaQuestion

# Configure logging settings
logging.basicConfig(level=logging.DEBUG)

def index(request):
    return render(request, 'game/index.html')

def game_view(request):
    logging.debug("Entered game_view function")

    if request.method == 'POST':
        logging.debug("Received POST request")

        # Handle answer submission
        question = request.POST.get('question')
        user_answer = request.POST.get('option')
        correct_answer = request.POST.get('answer_label')

        if user_answer == correct_answer:
            messages.success(request, 'Correct answer')
            return handle_next_question(request)
        else:
            attempts = request.session.get('attempts', 0)
            request.session['attempts'] = attempts + 1

            if attempts >= 2:  # User has no further attempts left
                messages.warning(request, f'Wrong answer, Correct Answer is {correct_answer}')
                return handle_next_question(request)

            messages.warning(request, f'Wrong answer, try again. Attempts remaining: {2 - attempts}')

    # Fetch a new question if no answer was submitted or the answer was incorrect
    response = fetch_question()
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if results:
            for result in results:
                # Save the question and its answers
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

    # Display the next question
    question_counter = request.session.get('question_counter', 0)
    attempts = request.session.get('attempts', 0)
    current_question_id = request.session.get('current_question')

    logging.debug(f"Question counter: {question_counter}")
    logging.debug(f"Attempts: {attempts}")
    logging.debug(f"Current question ID: {current_question_id}")

    question = TriviaQuestion.objects.order_by('?').first()
    return render(request, 'game/game_screen.html', {'question': question})

def handle_next_question(request):
    question_counter = request.session.get('question_counter', 0)
    request.session['question_counter'] = question_counter + 1

    request.session['attempts'] = 0  # Reset attempts for the new question

    if question_counter >= 9:  # Max questions for the game (starting from 0)
        return render(request, 'game/game_finished.html')

    return redirect('game_view')
