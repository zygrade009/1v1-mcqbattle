from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GameResultSerializer
from .models import GameResult
from GameSession.models import GameSession, Participant

class EndGameView(APIView):
    def post(self, request, session_id):
        try:
            game_session = GameSession.objects.get(pk=session_id)
            participants = Participant.objects.filter(game_session=game_session)
            final_scores = {p.user.username: p.score for p in participants}
            winner = max(participants, key=lambda p: p.score)

            result = GameResult.objects.create(
                game_session=game_session,
                winner=winner,
                final_scores=final_scores
            )

            game_session.is_active = False  # Mark session as inactive
            game_session.save()

            return Response(GameResultSerializer(result).data)
        except GameSession.DoesNotExist:
            return Response({'error': 'Game session not found.'}, status=status.HTTP_404_NOT_FOUND)


class GameResultView(generics.RetrieveAPIView):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    lookup_field = 'game_session__id'  # Lookup by session ID
