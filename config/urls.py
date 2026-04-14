from django.contrib import admin
from django.urls import path, include
from apps.games.urls import leaderboard_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    # Games — /api/games/
    path('api/games/', include('apps.games.urls')),

    # Leaderboard — /api/leaderboard/
    path('api/leaderboard/', include(leaderboard_urlpatterns)),
]
