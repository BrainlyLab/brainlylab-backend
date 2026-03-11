from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Game, Score
from .serializers import (
    GameListSerializer,
    GameDetailSerializer,
    ScoreSubmitSerializer,
    ScoreSerializer,
    LeaderboardEntrySerializer,
)


class LeaderboardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


def get_active_game_or_404(slug):
    return get_object_or_404(Game, slug=slug, is_active=True)


def build_leaderboard_entries(paginator, page, request):
    """Shared rank assignment logic for both leaderboard views."""
    page_number = max(1, int(request.query_params.get(paginator.page_query_param, 1) or 1))
    offset = (page_number - 1) * paginator.page_size

    entries = [
        {
            'rank': offset + i,
            'user_id': row['user__id'],
            'username': row['user__username'],
            'total_score': row['total_score'],
        }
        for i, row in enumerate(page, start=1)
    ]
    return entries


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------

class GameListView(APIView):
    """GET /api/games/"""
    permission_classes = [AllowAny]

    def get(self, request):
        games = Game.objects.filter(is_active=True)
        return Response(GameListSerializer(games, many=True).data)


class GameDetailView(APIView):
    """GET /api/games/<slug>/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        game = get_object_or_404(
            Game.objects.annotate(total_plays=Count('scores')),
            slug=slug,
            is_active=True,
        )
        return Response(GameDetailSerializer(game).data)


class SubmitScoreView(APIView):
    """POST /api/games/<slug>/submit-score/"""
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        game = get_active_game_or_404(slug)

        serializer = ScoreSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score = Score.objects.create(
            user=request.user,
            game=game,
            score=serializer.validated_data['score'],
        )

        return Response(
            ScoreSerializer(score).data,
            status=status.HTTP_201_CREATED,
        )


class MyScoresView(APIView):
    """GET /api/games/<slug>/my-scores/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        game = get_active_game_or_404(slug)

        scores = Score.objects.filter(
            user=request.user, game=game,
        ).order_by('-submitted_at')

        paginator = LeaderboardPagination()
        page = paginator.paginate_queryset(scores, request)
        return paginator.get_paginated_response(ScoreSerializer(page, many=True).data)


# ---------------------------------------------------------------------------
# Leaderboard — query-based, no separate table
# ---------------------------------------------------------------------------

class GlobalLeaderboardView(APIView):
    """GET /api/leaderboard/"""
    permission_classes = [AllowAny]

    def get(self, request):
        qs = (
            Score.objects
            .values('user__id', 'user__username')
            .annotate(total_score=Sum('score'))
            .order_by('-total_score')
        )

        paginator = LeaderboardPagination()
        page = paginator.paginate_queryset(qs, request)
        entries = build_leaderboard_entries(paginator, page, request)

        return paginator.get_paginated_response(
            LeaderboardEntrySerializer(entries, many=True).data
        )


class GameLeaderboardView(APIView):
    """GET /api/leaderboard/<game_slug>/"""
    permission_classes = [AllowAny]

    def get(self, request, game_slug):
        game = get_active_game_or_404(game_slug)

        qs = (
            Score.objects
            .filter(game=game)
            .values('user__id', 'user__username')
            .annotate(total_score=Sum('score'))
            .order_by('-total_score')
        )

        paginator = LeaderboardPagination()
        page = paginator.paginate_queryset(qs, request)
        entries = build_leaderboard_entries(paginator, page, request)

        return paginator.get_paginated_response(
            LeaderboardEntrySerializer(entries, many=True).data
        )
