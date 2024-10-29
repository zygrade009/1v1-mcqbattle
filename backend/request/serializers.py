from rest_framework import serializers
from .models import JoinRequest
from game_model.models import Game
class JoinRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.SerializerMethodField()
    game = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.ChoiceField(choices=JoinRequest.STATUS_CHOICES, default='pending')

    def get_user(self, obj):
        return obj.user.first_name

    def get_game(self, obj):
        return obj.game.game_name

    def create(self, validated_data):
        user = self.context['request'].user  # Get the current user from the request context
        game_id = self.context['game_id']  # Assuming the game ID is passed in the context
        game = Game.objects.get(game_id=game_id)
        join_request = JoinRequest.objects.create(user=user, game=game, **validated_data)
        return join_request

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.first_name
        representation['game'] = instance.game.game_name
        return representation
