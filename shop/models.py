from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # "skin" or "item"
    price_coins = models.IntegerField()
    image_url = models.URLField(max_length=500)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=\'inventory\')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User Inventories"

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=\'transactions\')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    coins_spent = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.item.name} for {self.coins_spent}"
