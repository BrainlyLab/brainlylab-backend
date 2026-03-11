from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('<slug:slug>/', views.GameDetailView.as_view(), name='game-detail'),
    path('<slug:slug>/submit-score/', views.SubmitScoreView.as_view(), name='submit-score'),
    path('<slug:slug>/my-scores/', views.MyScoresView.as_view(), name='my-scores'),
]

leaderboard_urlpatterns = [
    path('', views.GlobalLeaderboardView.as_view(), name='global-leaderboard'),
    path('<slug:game_slug>/', views.GameLeaderboardView.as_view(), name='game-leaderboard'),
]
