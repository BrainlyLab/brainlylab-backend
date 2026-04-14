from django.contrib import admin
from .models import Game, Score


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at',)
    list_filter = ('is_active',)
    search_fields = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'score', 'submitted_at',)
    list_filter = ('game',)
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    readonly_fields = ('submitted_at',)
