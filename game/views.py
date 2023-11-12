from django.shortcuts import redirect, render

from game.utils import fetch_questions


def index(request):
	return render(request, 'game/index.html')


def game(request):
	difficulty_levels = ["easy", "medium", "hard"]
	questions = fetch_questions(difficulty_levels)
	context = {
		"questions": questions
	}
	return render(request, 'game/game_screen.html')
