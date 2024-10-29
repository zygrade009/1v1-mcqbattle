import pusher
from mcqbattle.settings import PUSHER_APP_ID,PUSHER_CLUSTER,PUSHER_KEY,PUSHER_SECRET
pusher_client = pusher.Pusher(
  app_id=PUSHER_APP_ID,
  key=PUSHER_KEY,
  secret=PUSHER_SECRET,
  cluster=PUSHER_CLUSTER,
  ssl=True
)
import logging

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import JoinRequest, Game
from .serializers import JoinRequestSerializer

class JoinRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
         # Get the current logged-in user
        user = request.user
        game_owned=Game.objects.filter(owner=user)
        join_requests = JoinRequest.objects.filter(game__in=game_owned)
        serializer = JoinRequestSerializer(join_requests, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        game_id = request.data.get('game_id')  # Assuming game_id is passed in the request data
        if not game_id:
            return Response({"detail": "game_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = JoinRequestSerializer(data=request.data, context={'request': request, 'game_id': game_id})
        if serializer.is_valid():
            join_request = serializer.save()
            return Response(JoinRequestSerializer(join_request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinRequestRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        logger.debug(f"Attempting to retrieve JoinRequest with pk: {pk}")
        try:
            return JoinRequest.objects.get(pk=pk)
        except JoinRequest.DoesNotExist:
            return None

    def get(self, request, pk):
        join_request = self.get_object(pk)
        if join_request is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JoinRequestSerializer(join_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
       
        join_request = self.get_object(pk)
        if join_request is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JoinRequestSerializer(join_request, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        
        join_request = self.get_object(pk)
        
        if join_request is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        join_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
