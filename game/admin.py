from django.contrib import admin
from .models import Player, Game, Question, AnswersSet
# Register your models here.

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Question)
admin.site.register(AnswersSet)
