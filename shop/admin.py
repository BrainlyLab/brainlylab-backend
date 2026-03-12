from django.contrib import admin
from .models import Item, UserInventory, Transaction

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'price_coins', 'is_available'
    )
    list_filter = ('type', 'is_available')
    search_fields = ('name', 'type')

@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'purchased_at')
    list_filter = ('purchased_at',)
    search_fields = ('user__username', 'item__name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'coins_spent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'item__name')
