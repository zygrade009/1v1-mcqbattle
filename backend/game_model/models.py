from django.utils import timezone
import uuid
from django.db import models
from auth_app.models import User
from datetime import timedelta
class Game(models.Model):
    GAME_STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    game_name = models.CharField(max_length=255, default='Unnamed Game')
    status = models.CharField(max_length=10, choices=GAME_STATUS_CHOICES, default='waiting')
    participants = models.ManyToManyField(User, related_name='participating_games', blank=True)
    expiration_time = models.DurationField(default=timedelta(seconds=1))
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.game_name} by {self.owner} - {self.status}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' or self.is_expired():
            self.joinrequest_set.all().delete()
            self.delete()
        super().save(*args, **kwargs)
    def is_expired(self):
        if self.created_at and self.expiration_time:
            expiration_datetime = self.created_at + self.expiration_time
            return timezone.now() > expiration_datetime
        return False

 