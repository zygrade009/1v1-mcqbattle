# urls.py
from django.contrib import admin
from django.urls import path , include

from auth_app.views import LoginView, ProtectedView, RegisterView
from GameSession.views import MCQDeliveryView, SubmitAnswerView
from GameResult.views import EndGameView, GameResultView
from request.views import JoinRequestListView, JoinRequestRetrieveUpdateDestroyView
from game_model.views import GameListView
from mcqs.views import MCQListCreateView, MCQRetrieveUpdateDestroyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("protected", ProtectedView.as_view(), name="protected"),
    path("mcqs", MCQListCreateView.as_view(), name="mcq-list-create"),
    path("mcqs/<uuid:pk>", MCQRetrieveUpdateDestroyView.as_view(), name="mcq-detail"),
    path("games", include('game_model.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request', JoinRequestListView.as_view(), name='join-request-list'),
    path('request/<uuid:pk>', JoinRequestRetrieveUpdateDestroyView.as_view(), name='join-request-detail'),
    path('game_session/<int:session_id>/next_mcq/', MCQDeliveryView.as_view(), name='next_mcq'),
    path('game_session/<int:session_id>/submit_answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('game_result/<int:session_id>/end_game/', EndGameView.as_view(), name='end_game'),
    path('game_result/<int:session_id>/results/', GameResultView.as_view(), name='results'),
]
