from django.contrib import admin
from .models import Game, Question, GameResult

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'xp_reward', 'plays_count', 'is_active']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['title']
    inlines = [QuestionInline]

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'correct_answers', 'total_questions', 'xp_earned', 'played_at']
    list_filter = ['game']
    ordering = ['-played_at']
