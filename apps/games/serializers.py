from rest_framework import serializers
from .models import Game, Score


class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'slug', 'description', 'is_active', 'created_at',)


class GameDetailSerializer(serializers.ModelSerializer):
    total_plays = serializers.IntegerField(read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'slug', 'description', 'is_active', 'created_at', 'total_plays',)


class ScoreSubmitSerializer(serializers.Serializer):
    score = serializers.IntegerField(min_value=0)


class ScoreSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='game.name', read_only=True)
    game_slug = serializers.CharField(source='game.slug', read_only=True)

    class Meta:
        model = Score
        fields = ('id', 'game_name', 'game_slug', 'score', 'submitted_at',)


class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    total_score = serializers.IntegerField(read_only=True)
