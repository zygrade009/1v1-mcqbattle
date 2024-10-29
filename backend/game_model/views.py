import pusher
from mcqbattle.settings import PUSHER_APP_ID,PUSHER_CLUSTER,PUSHER_KEY,PUSHER_SECRET
pusher_client = pusher.Pusher(
  app_id=PUSHER_APP_ID,
  key=PUSHER_KEY,
  secret=PUSHER_SECRET,
  cluster=PUSHER_CLUSTER,
  ssl=True
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view, permission_classes

class GameListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        games = Game.objects.all()
        for game in games:
            if game.is_expired():
                game.delete()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GameSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            game = serializer.save()
            print(pusher)
            pusher_client.trigger('lobby','all-games',{"message":"all-games"})
            return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GameRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return None

    def get(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
         
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        game.delete()
      
        return Response(status=status.HTTP_204_NO_CONTENT)
