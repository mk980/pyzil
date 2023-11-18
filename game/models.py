from django.db import models


# Create your models here.

class Player(models.Model):
	game = models.ForeignKey('Game', on_delete=models.PROTECT)


class Game(models.Model):
	question = models.ForeignKey('Question', on_delete=models.PROTECT)
	score = models.IntegerField(null=True, blank=True, default=0)


class Question(models.Model):
	answer_set = models.OneToOneField(
		'AnswersSet',
		on_delete=models.CASCADE,
		primary_key=True,
	)


class TriviaQuestion(models.Model):
	category = models.CharField(max_length=200, null=False, blank=False)
	difficulty = models.CharField(max_length=10, null=False, blank=False)
	question = models.TextField(max_length=500, null=False, blank=False)
	type = models.CharField(max_length=15, null=False, blank=False)
	answer_set = models.OneToOneField(
		'AnswersSet',
		on_delete=models.CASCADE,
		primary_key=True)


class AnswersSet(models.Model):
	correct_answer = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer1 = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer2 = models.CharField(max_length=128, null=False, blank=False)
	incorrect_answer3 = models.CharField(max_length=128, null=False, blank=False)


class CategoryList(models.Model):
	category_id = models.CharField(max_length=5)
	name = models.CharField(max_length=50)
	trivia_question = models.ForeignKey(
		'TriviaQuestion',
		blank=False,
		on_delete=models.CASCADE,
	)
