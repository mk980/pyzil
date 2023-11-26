from django.test import TestCase
from django.urls import reverse
from .models import TriviaQuestion, AnswersSet, GameSession


class TriviaQuestionModelTestCase(TestCase):
    def setUp(self):
        self.game_session = GameSession.objects.create()
        self.answers_set = AnswersSet.objects.create(
            correct_answer='Correct Answer',
            incorrect_answer1='Incorrect Answer 1',
            incorrect_answer2='Incorrect Answer 2',
            incorrect_answer3='Incorrect Answer 3'
        )
        self.trivia_question = TriviaQuestion.objects.create(
            user_answer='User Answer',
            category='Category',
            difficulty='Easy',
            question='Sample Question',
            type='Multiple Choice',
            is_answered=True,
            answer_set=self.answers_set
        )

        self.game_session.game_questions.add(self.trivia_question)
        self.game_session.save()

    def test_trivia_question_creation(self):
        self.assertEqual(self.trivia_question.user_answer, 'User Answer')
        self.assertEqual(self.trivia_question.category, 'Category')
        self.assertEqual(self.trivia_question.difficulty, 'Easy')
        self.assertEqual(self.trivia_question.question, 'Sample Question')
        self.assertEqual(self.trivia_question.type, 'Multiple Choice')
        self.assertTrue(self.trivia_question.is_answered)
        self.assertEqual(self.trivia_question.answer_set, self.answers_set)

    def test_str_representation(self):
        expected_str = f"{self.trivia_question.question} ({self.trivia_question.category})"
        self.assertEqual(str(self.trivia_question), expected_str)

    def test_trivia_question_is_related_to_game_session(self):
        self.assertTrue(self.trivia_question in self.game_session.game_questions.all())


class GameViewTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/index.html')

    def test_game_view_get(self):
        response = self.client.get(reverse('game_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/game_screen.html')
