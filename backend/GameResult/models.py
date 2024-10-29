from django.db import models
from GameSession.models import GameSession, Participant

class GameResult(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='results')
    winner = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, related_name='won_games')
    final_scores = models.JSONField()

    def __str__(self):
        return f"Result for {self.game_session} - Winner: {self.winner.user.username if self.winner else 'None'}"
