import logging
from django.shortcuts import render
from .utils import fetch_question
from .models import AnswersSet, TriviaQuestion, GameSession

logging.basicConfig(level=logging.DEBUG)


def index(request):
    return render(request, 'game/index.html')


def new_game_start(request):
    response = fetch_question()
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        new_game = GameSession()
        new_game.save()
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
                    answer_set=answers_set,

                )
                question.save()
                new_game.game_questions.add(question)
                new_game.save()
        question = new_game.game_questions.first()
        return render(request,
                      'game/game_screen.html',
                      {'question': question,
                       "game_id": new_game.pk,
                       'current_question_id': question.pk})


def game_view(request):
    logging.debug("Entered game_view function")
    logging.debug(request.session.items())
    log_items = {key: value for key, value in request.session.items() if key != 'asked_questions'}
    logging.debug(log_items)

    if request.method == "GET":
        return new_game_start(request)

    if request.method == 'POST':
        logging.debug("Received POST request")
        current_question_id = request.session.get('current_question')
        user_answer = request.POST.get('option')
        question = get_current_question(request)
        question.user_answer = user_answer
        question.is_answered = True
        question.save()

        next_question = get_next_question(request)
        if next_question == None:
            score = 0
            game = GameSession.objects.get(pk=request.POST.get("game_id"))
            for question in game.game_questions.all():
                if question.user_answer == question.answer_set.correct_answer:
                    score += 1

            return render(request, "game/game_finished.html",
                          {'score': score, "questioncount": game.game_questions.count()})
        else:
            return render(request,
                          'game/game_screen.html',
                          {'question': next_question, 'current_question_id': current_question_id,
                           "game_id": request.POST.get("game_id")})


def get_current_question(request):
    current_question_id = request.POST.get("current_question")
    print(current_question_id)
    return TriviaQuestion.objects.get(pk=current_question_id)


def get_next_question(request):
    current_game = GameSession.objects.get(pk=request.POST.get("game_id"))
    unanswered_questions = current_game.game_questions.filter(is_answered=False)
    if unanswered_questions.count() > 0:
        return unanswered_questions.first()




