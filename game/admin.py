from django.contrib import admin
from .models import Player, Game, AnswersSet, TriviaQuestion

# Register your models here.

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(AnswersSet)
admin.site.register(TriviaQuestion)


