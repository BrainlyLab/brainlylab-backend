from django.conf import settings
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'games'
        ordering = ['name']

    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scores',
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='scores',
    )
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scores'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['game', '-score'], name='idx_score_game_desc'),
            models.Index(fields=['user', 'game', '-submitted_at'], name='idx_score_user_game'),
            models.Index(fields=['user', '-score'], name='idx_score_user_desc'),
        ]

    def __str__(self):
        return f"{self.user} — {self.game} — {self.score}pts"
