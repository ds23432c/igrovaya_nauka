from django.contrib import admin
from .models import Achievement, UserAchievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'category', 'condition_type', 'condition_value', 'xp_reward', 'is_active']
    list_filter = ['category', 'is_active']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    ordering = ['-earned_at']
