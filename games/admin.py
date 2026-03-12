from django.contrib import admin
from .models import Game, Score

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'is_active', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'game', 'score', 'submitted_at'
    )
    list_filter = ('game', 'submitted_at')
    search_fields = ('user__username', 'game__name')
    date_hierarchy = 'submitted_at'
