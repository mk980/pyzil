from django.contrib import admin
from .models import AnswersSet, TriviaQuestion, GameSession

# Register your models here.


admin.site.register(AnswersSet)
admin.site.register(TriviaQuestion)
admin.site.register(GameSession)


