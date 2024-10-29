from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GameSession, Participant
from .serializers import GameSessionSerializer, MCQSerializer
from mcqs.models import MCQ
import random

class MCQDeliveryView(APIView):
    def get(self, request, session_id):
        try:
            game_session = GameSession.objects.get(pk=session_id, is_active=True)
            mcq = random.choice(MCQ.objects.all())  # Fetch a random MCQ
            game_session.current_question = mcq
            game_session.save()
            return Response(MCQSerializer(mcq).data)
        except GameSession.DoesNotExist:
            return Response({'error': 'Game session not found or inactive.'}, status=status.HTTP_404_NOT_FOUND)


class SubmitAnswerView(APIView):
    def post(self, request, session_id):
        try:
            game_session = GameSession.objects.get(pk=session_id, is_active=True)
            participant = Participant.objects.get(user=request.user, game_session=game_session)
            answer = request.data.get('answer')
            correct_answer = game_session.current_question.correct_answer  # Assuming MCQ has correct_answer field
            
            if answer == correct_answer:
                participant.score += 1
            else:
                participant.incorrect_answers += 1
            
            participant.save()

            if participant.incorrect_answers >= 3:
                game_session.is_active = False  # End game if participant gets 3 incorrect answers
                game_session.save()

            return Response({'message': 'Answer submitted successfully.', 'score': participant.score})
        except (GameSession.DoesNotExist, Participant.DoesNotExist):
            return Response({'error': 'Game session or participant not found.'}, status=status.HTTP_404_NOT_FOUND)
