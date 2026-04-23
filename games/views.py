from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Game, Score
from .serializers import GameSerializer, ScoreSerializer
from users.models import BrainlyCoins, UserProfile
from users.serializers import BrainlyCoinsSerializer

class GameListAPIView(generics.ListAPIView):
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]

class GameDetailAPIView(generics.RetrieveAPIView):
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class SubmitScoreAPIView(generics.CreateAPIView):
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        game_slug = self.kwargs.get('slug')
        game = get_object_or_404(Game, slug=game_slug, is_active=True)
        score_value = request.data.get('score')

        try:
            score_value = int(score_value)
        except (ValueError, TypeError):
            return Response({'error': 'Score must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if score_value < 0:
            return Response({'error': 'Score cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            score_obj = Score.objects.create(
                user=request.user,
                game=game,
                score=score_value
            )
            coins_to_award = max(1, score_value // 100)
            reason = f"Score of {score_value} in {game.name}"
            history = BrainlyCoins.objects.create(
                user=request.user,
                coins_earned=coins_to_award,
                reason=reason
            )
            profile = request.user.profile
            profile.brainlycoins += coins_to_award
            profile.save()

        serializer = self.get_serializer(score_obj)
        return Response({
            'score': serializer.data,
            'coins_awarded': coins_to_award
        }, status=status.HTTP_201_CREATED)

class MyScoresAPIView(generics.ListAPIView):
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        game_slug = self.kwargs.get('slug')
        game = get_object_or_404(Game, slug=game_slug)
        return Score.objects.filter(user=self.request.user, game=game).order_by('-submitted_at')
