from django.urls import path
from .views import GameListView, GameRetrieveUpdateDestroyView

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('<uuid:pk>/', GameRetrieveUpdateDestroyView.as_view(), name='game-detail'),
]
