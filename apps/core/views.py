from django.shortcuts import render
from apps.games.models import Game, GameResult
from apps.courses.models import Course
from apps.accounts.models import User


def home(request):
    featured_games = Game.objects.filter(is_active=True).order_by('-plays_count')[:6]
    featured_courses = Course.objects.filter(is_published=True)[:4]
    top_players = User.objects.filter(is_active=True).order_by('-xp')[:5]
    recent_results = GameResult.objects.select_related('user', 'game').order_by('-played_at')[:5]
    return render(request, 'core/home.html', {
        'featured_games': featured_games,
        'featured_courses': featured_courses,
        'top_players': top_players,
        'recent_results': recent_results,
    })


def about(request):
    return render(request, 'core/about.html')
