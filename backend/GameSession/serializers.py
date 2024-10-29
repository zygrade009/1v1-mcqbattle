from rest_framework import serializers
from .models import GameSession, Participant
from mcqs.models import MCQ
from auth_app.models import User  # Ensure you're importing the custom User model
from game_model.models import Game  # Ensure you import Game model if used

class MCQSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    body = serializers.CharField()
    options = serializers.JSONField()  # Assuming options is a JSONField

class ParticipantSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Reference your custom User model
    score = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()

class GameSessionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    participants = ParticipantSerializer(many=True, read_only=True)
    current_question = MCQSerializer(read_only=True)
    start_time = serializers.DateTimeField()
    is_active = serializers.BooleanField()

    def create(self, validated_data):
        game = validated_data['game']
        session = GameSession.objects.create(**validated_data)
        return session

    def update(self, instance, validated_data):
        instance.game = validated_data.get('game', instance.game)
        instance.current_question = validated_data.get('current_question', instance.current_question)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
