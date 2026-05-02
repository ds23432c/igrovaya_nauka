from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.games.models import Game, Question, GameResult
from apps.courses.models import Course, Lesson
from apps.achievements.models import Achievement


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.role == 'admin'):
            from django.contrib.auth import logout
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    stats = {
        'total_users': User.objects.count(),
        'new_users_week': User.objects.filter(date_joined__gte=week_ago).count(),
        'total_games': Game.objects.count(),
        'total_courses': Course.objects.count(),
        'total_results': GameResult.objects.count(),
        'results_week': GameResult.objects.filter(played_at__gte=week_ago).count(),
    }
    top_games = Game.objects.order_by('-plays_count')[:5]
    recent_users = User.objects.order_by('-date_joined')[:10]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'top_games': top_games,
        'recent_users': recent_users,
    })


@admin_required
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@admin_required
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    status = 'активирован' if user.is_active else 'заблокирован'
    messages.success(request, f'Пользователь {user.username} {status}')
    return redirect('admin_panel:users')


@admin_required
def games_list(request):
    games = Game.objects.annotate(result_count=Count('results')).order_by('-created_at')
    return render(request, 'admin_panel/games.html', {'games': games})


@admin_required
def game_edit(request, pk=None):
    game = get_object_or_404(Game, pk=pk) if pk else None
    if request.method == 'POST':
        data = request.POST
        if game:
            game.title = data['title']
            game.description = data['description']
            game.category = data['category']
            game.difficulty = data['difficulty']
            game.game_type = data['game_type']
            game.cover_url = data['cover_url']
            game.xp_reward = int(data.get('xp_reward', 50))
            game.is_active = 'is_active' in data
            game.save()
            messages.success(request, 'Игра обновлена!')
        else:
            game = Game.objects.create(
                title=data['title'], description=data['description'],
                category=data['category'], difficulty=data['difficulty'],
                game_type=data['game_type'], cover_url=data['cover_url'],
                xp_reward=int(data.get('xp_reward', 50)),
            )
            messages.success(request, 'Игра создана!')
        return redirect('admin_panel:games')
    return render(request, 'admin_panel/game_edit.html', {
        'game': game,
        'categories': Game.CATEGORY_CHOICES,
        'difficulties': Game.DIFFICULTY_CHOICES,
        'types': Game.TYPE_CHOICES,
    })


@admin_required
def courses_list(request):
    courses = Course.objects.annotate(enrolled=Count('enrollments')).order_by('-created_at')
    return render(request, 'admin_panel/courses.html', {'courses': courses})


@admin_required
def achievements_list(request):
    achievements = Achievement.objects.all().order_by('-id')
    return render(request, 'admin_panel/achievements.html', {'achievements': achievements})
