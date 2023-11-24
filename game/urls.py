from django.urls import path


from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path("game_screen/", views.game_view, name='game_view'),
	path("incorrect_answer/", views.game_view, name='game_view')
]