from django.urls import path
from .views import GameListAPIView, GameDetailAPIView, SubmitScoreAPIView, MyScoresAPIView

urlpatterns = [
    path('', GameListAPIView.as_view(), name='game-list'),
    path('<slug:slug>/', GameDetailAPIView.as_view(), name='game-detail'),
    path('<slug:slug>/submit-score/', SubmitScoreAPIView.as_view(), name='submit-score'),
    path('<slug:slug>/my-scores/', MyScoresAPIView.as_view(), name='my-scores'),
]
