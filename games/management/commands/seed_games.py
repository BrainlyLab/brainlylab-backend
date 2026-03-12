from django.core.management.base import BaseCommand
from games.models import Game
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed the database with 11 games'

    def handle(self, *args, **kwargs):
        games_data = [
            {"name": "Memory Match", "description": "Test your memory by matching pairs of cards."},
            {"name": "Speed Math", "description": "Solve as many math problems as you can in 60 seconds."},
            {"name": "Word Scramble", "description": "Unscramble the letters to find the hidden word."},
            {"name": "Pattern Recognition", "description": "Identify the next shape or number in the sequence."},
            {"name": "Logic Puzzles", "description": "Solve challenging logic-based riddles."},
            {"name": "Geography Quiz", "description": "Identify countries, capitals, and landmarks."},
            {"name": "Typing Master", "description": "Improve your typing speed and accuracy."},
            {"name": "Color Blind", "description": "Pick the odd color out from the grid."},
            {"name": "Sudoku", "description": "Classic number placement puzzle."},
            {"name": "Trivia Challenge", "description": "General knowledge questions across various topics."},
            {"name": "Reaction Time", "description": "Click as fast as you can when the screen turns green."},
        ]

        for game_info in games_data:
            game, created = Game.objects.get_or_create(
                name=game_info["name"],
                defaults={
                    "slug": slugify(game_info["name"]),
                    "description": game_info["description"],
                    "is_active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created game: {game.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Game already exists: {game.name}'))
