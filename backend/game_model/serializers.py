from rest_framework import serializers
from .models import Game
from datetime import timedelta

class GameSerializer(serializers.Serializer):
    game_id = serializers.UUIDField(read_only=True)
    game_name = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=Game.GAME_STATUS_CHOICES, default='waiting')
    owner = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    expiration_time = serializers.DurationField()  # Adjusted for DurationField

    def get_owner(self, obj):
        return obj.owner.first_name

    def get_participants(self, obj):
        return [user.first_name for user in obj.participants.all()]

    def create(self, validated_data):
        owner = self.context['request'].user  # Get the current user from the request context
        game = Game.objects.create(owner=owner, **validated_data)
        return game

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert expiration_time from a timedelta to a more human-readable format if needed
        representation['expiration_time'] = str(instance.expiration_time)
        return representation
