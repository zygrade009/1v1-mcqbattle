from django.db import models
from auth_app.models import User
from mcqs.models import MCQ  # Assuming MCQ is in the mcq app
from game_model.models import Game  # Assuming Game is in the game_model app

class GameSession(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    participants = models.ManyToManyField(User, through='Participant')
    current_question = models.ForeignKey(MCQ, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session for {self.game} - Active: {self.is_active}"


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} in session {self.game_session} - Score: {self.score}"
