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
    difficulty_level = models.CharField(max_length=32, null=False, blank=False)


class AnswersSet(models.Model):
    correct_answer = models.CharField(max_length=128, null=False, blank=False)
    incorrect_answer1 = models.CharField(max_length=128, null=False, blank=False)
    incorrect_answer2 = models.CharField(max_length=128, null=False, blank=False)
    incorrect_answer3 = models.CharField(max_length=128, null=False, blank=False)