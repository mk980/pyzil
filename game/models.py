from django.db import models


class TriviaQuestion(models.Model):
	user_answer = models.CharField(max_length=128, null=True, blank=True)
	category = models.CharField(max_length=200, null=False, blank=False)
	difficulty = models.CharField(max_length=10, null=False, blank=False)
	question = models.TextField(max_length=500, null=False, blank=False)
	type = models.CharField(max_length=15, null=False, blank=False)
	is_answered = models.BooleanField(null=False, blank=False, default=False)
	answer_set = models.OneToOneField(
		'AnswersSet',
		on_delete=models.CASCADE,
		primary_key=True)

	def __str__(self):
		return f"{self.question} ({self.category})"


class AnswersSet(models.Model):
	correct_answer = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer1 = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer2 = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer3 = models.CharField(max_length=128, null=False, blank=False)


class GameSession(models.Model):
	name = models.CharField(max_length=128, null=False, blank=False, default="New Game")
	game_questions = models.ManyToManyField(TriviaQuestion, blank=True)
