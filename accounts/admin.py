from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, BrainlyCoins

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'brainlycoins', 'created_at')
    search_fields = ('user__username',)

@admin.register(BrainlyCoins)
class BrainlyCoinsAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins_earned', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('user__username', 'reason')
    date_hierarchy = 'created_at'
