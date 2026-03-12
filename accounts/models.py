from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(max_length=500, blank=True, null=True)
    brainlycoins = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class BrainlyCoins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coin_transactions')
    coins_earned = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Brainly Coins"

    def __str__(self):
        return f"{self.user.username} - {self.coins_earned} coins ({self.reason})"
