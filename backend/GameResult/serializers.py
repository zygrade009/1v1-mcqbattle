from rest_framework import serializers
from .models import GameResult
from GameSession.models import GameSession
from GameSession.models import Participant

class GameResultSerializer(serializers.Serializer):
    game_session = serializers.PrimaryKeyRelatedField(queryset=GameSession.objects.all())
    winner = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all(), required=False, allow_null=True)
    final_scores = serializers.JSONField()

    def create(self, validated_data):
        result = GameResult.objects.create(**validated_data)
        return result

    def update(self, instance, validated_data):
        instance.game_session = validated_data.get('game_session', instance.game_session)
        instance.winner = validated_data.get('winner', instance.winner)
        instance.final_scores = validated_data.get('final_scores', instance.final_scores)
        instance.save()
        return instance
