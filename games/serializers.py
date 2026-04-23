from rest_framework import serializers
from .models import Game, Score

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at']

class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    game = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'user', 'game', 'score', 'submitted_at']
        read_only_fields = ['id', 'user', 'game', 'submitted_at']
