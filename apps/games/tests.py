"""
Games & Leaderboard tests

    python manage.py test apps.games -v2
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Game, Score

User = get_user_model()


def _make_auth_client(username='player1', email='p1@bl.com', password='TestPass123!'):
    """Create user + return authenticated client using force_authenticate."""
    user = User.objects.create_user(username=username, email=email, password=password)
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


# ---------------------------------------------------------------------------
# Game endpoints
# ---------------------------------------------------------------------------

class GameListTests(TestCase):

    def setUp(self):
        self.c = APIClient()
        Game.objects.create(name='Math Blitz', slug='math-blitz', is_active=True)
        Game.objects.create(name='Hidden Game', slug='hidden', is_active=False)

    def test_lists_active_only(self):
        r = self.c.get('/api/games/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]['slug'], 'math-blitz')

    def test_fields_present(self):
        r = self.c.get('/api/games/')
        game = r.data[0]
        for field in ('id', 'name', 'slug', 'description', 'is_active', 'created_at'):
            self.assertIn(field, game)


class GameDetailTests(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.game = Game.objects.create(name='Quiz', slug='quiz')

    def test_get_detail(self):
        r = self.c.get('/api/games/quiz/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['slug'], 'quiz')
        self.assertEqual(r.data['total_plays'], 0)

    def test_not_found(self):
        r = self.c.get('/api/games/nonexistent/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactive_not_found(self):
        Game.objects.create(name='Dead', slug='dead', is_active=False)
        r = self.c.get('/api/games/dead/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_total_plays_count(self):
        user = User.objects.create_user(username='u', email='u@t.com', password='x')
        Score.objects.create(user=user, game=self.game, score=100)
        Score.objects.create(user=user, game=self.game, score=200)
        r = self.c.get('/api/games/quiz/')
        self.assertEqual(r.data['total_plays'], 2)


# ---------------------------------------------------------------------------
# Score submission
# ---------------------------------------------------------------------------

class ScoreSubmitTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create(name='Math', slug='math')

    def test_submit_score(self):
        c, user = _make_auth_client()
        r = c.post('/api/games/math/submit-score/', {'score': 850}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['score'], 850)
        self.assertEqual(Score.objects.count(), 1)

    def test_reject_negative_score(self):
        c, _ = _make_auth_client()
        r = c.post('/api/games/math/submit-score/', {'score': -10}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_missing_score(self):
        c, _ = _make_auth_client()
        r = c.post('/api/games/math/submit-score/', {}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_rejected(self):
        c = APIClient()
        r = c.post('/api/games/math/submit-score/', {'score': 100}, format='json')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_game_rejected(self):
        Game.objects.create(name='Dead', slug='dead', is_active=False)
        c, _ = _make_auth_client()
        r = c.post('/api/games/dead/submit-score/', {'score': 100}, format='json')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_game(self):
        c, _ = _make_auth_client()
        r = c.post('/api/games/fake/submit-score/', {'score': 100}, format='json')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_zero_score_accepted(self):
        c, _ = _make_auth_client()
        r = c.post('/api/games/math/submit-score/', {'score': 0}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# My scores
# ---------------------------------------------------------------------------

class MyScoresTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create(name='Quiz', slug='quiz')

    def test_empty_history(self):
        c, _ = _make_auth_client()
        r = c.get('/api/games/quiz/my-scores/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['count'], 0)

    def test_returns_own_scores_only(self):
        c1, user1 = _make_auth_client('alice', 'a@t.com')
        _, user2 = _make_auth_client('bob', 'b@t.com')

        Score.objects.create(user=user1, game=self.game, score=500)
        Score.objects.create(user=user1, game=self.game, score=700)
        Score.objects.create(user=user2, game=self.game, score=900)

        r = c1.get('/api/games/quiz/my-scores/')
        self.assertEqual(r.data['count'], 2)

    def test_unauthenticated(self):
        r = APIClient().get('/api/games/quiz/my-scores/')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_game(self):
        c, _ = _make_auth_client()
        r = c.get('/api/games/fake/my-scores/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Global leaderboard
# ---------------------------------------------------------------------------

class GlobalLeaderboardTests(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.game1 = Game.objects.create(name='Math', slug='math')
        self.game2 = Game.objects.create(name='Quiz', slug='quiz')

        # alice: 900 + 300 = 1200 total
        self.alice = User.objects.create_user(username='alice', email='a@t.com', password='x')
        Score.objects.create(user=self.alice, game=self.game1, score=900)
        Score.objects.create(user=self.alice, game=self.game2, score=300)

        # bob: 700 total
        self.bob = User.objects.create_user(username='bob', email='b@t.com', password='x')
        Score.objects.create(user=self.bob, game=self.game1, score=700)

        # charlie: 500 total
        self.charlie = User.objects.create_user(username='charlie', email='c@t.com', password='x')
        Score.objects.create(user=self.charlie, game=self.game1, score=500)

    def test_ranked_correctly(self):
        r = self.c.get('/api/leaderboard/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        results = r.data['results']
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['username'], 'alice')
        self.assertEqual(results[0]['total_score'], 1200)
        self.assertEqual(results[0]['rank'], 1)
        self.assertEqual(results[1]['username'], 'bob')
        self.assertEqual(results[1]['rank'], 2)
        self.assertEqual(results[2]['username'], 'charlie')
        self.assertEqual(results[2]['rank'], 3)

    def test_response_fields(self):
        r = self.c.get('/api/leaderboard/')
        entry = r.data['results'][0]
        for field in ('rank', 'user_id', 'username', 'total_score'):
            self.assertIn(field, entry)

    def test_pagination_present(self):
        r = self.c.get('/api/leaderboard/')
        for key in ('count', 'next', 'results'):
            self.assertIn(key, r.data)

    def test_empty_leaderboard(self):
        Score.objects.all().delete()
        r = self.c.get('/api/leaderboard/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['count'], 0)


# ---------------------------------------------------------------------------
# Per-game leaderboard
# ---------------------------------------------------------------------------

class GameLeaderboardTests(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.game = Game.objects.create(name='Math', slug='math')

        self.alice = User.objects.create_user(username='alice', email='a@t.com', password='x')
        self.bob = User.objects.create_user(username='bob', email='b@t.com', password='x')

        # alice played twice: 400 + 500 = 900
        Score.objects.create(user=self.alice, game=self.game, score=400)
        Score.objects.create(user=self.alice, game=self.game, score=500)

        # bob played once: 600
        Score.objects.create(user=self.bob, game=self.game, score=600)

    def test_per_game_ranking(self):
        r = self.c.get('/api/leaderboard/math/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        results = r.data['results']
        self.assertEqual(results[0]['username'], 'alice')
        self.assertEqual(results[0]['total_score'], 900)
        self.assertEqual(results[1]['username'], 'bob')
        self.assertEqual(results[1]['total_score'], 600)

    def test_nonexistent_game(self):
        r = self.c.get('/api/leaderboard/fake/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactive_game(self):
        Game.objects.create(name='Dead', slug='dead', is_active=False)
        r = self.c.get('/api/leaderboard/dead/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_scores_dont_leak_across_games(self):
        """Scores from other games shouldn't appear in per-game leaderboard."""
        other = Game.objects.create(name='Quiz', slug='quiz')
        Score.objects.create(user=self.alice, game=other, score=9999)

        r = self.c.get('/api/leaderboard/math/')
        results = r.data['results']
        # alice's math total should still be 900, not 900+9999
        self.assertEqual(results[0]['total_score'], 900)
