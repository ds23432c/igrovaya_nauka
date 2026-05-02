import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Game, Question, GameResult
from apps.achievements.utils import check_achievements


def games_list(request):
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    games = Game.objects.filter(is_active=True)
    if category:
        games = games.filter(category=category)
    if difficulty:
        games = games.filter(difficulty=difficulty)
    categories = Game.CATEGORY_CHOICES
    difficulties = Game.DIFFICULTY_CHOICES
    return render(request, 'games/list.html', {
        'games': games,
        'categories': categories,
        'difficulties': difficulties,
        'selected_category': category,
        'selected_difficulty': difficulty,
    })


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk, is_active=True)
    best_result = None
    if request.user.is_authenticated:
        best_result = GameResult.objects.filter(user=request.user, game=game).order_by('-score').first()
    recent_results = GameResult.objects.filter(game=game).select_related('user').order_by('-played_at')[:5]
    return render(request, 'games/detail.html', {
        'game': game,
        'best_result': best_result,
        'recent_results': recent_results,
    })


@login_required
def play_game(request, pk):
    game = get_object_or_404(Game, pk=pk, is_active=True)
    questions = list(game.questions.all().values('id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct', 'explanation'))
    game.plays_count += 1
    game.save(update_fields=['plays_count'])
    return render(request, 'games/play.html', {
        'game': game,
        'questions_json': json.dumps(questions, ensure_ascii=False),
    })


@login_required
@require_POST
def submit_result(request, pk):
    game = get_object_or_404(Game, pk=pk)
    try:
        data = json.loads(request.body)
        correct = int(data.get('correct', 0))
        total = int(data.get('total', 0))
        time_spent = int(data.get('time_spent', 0))
        score = int((correct / total) * 100) if total > 0 else 0
        xp = int((correct / total) * game.xp_reward) if total > 0 else 0

        result = GameResult.objects.create(
            user=request.user,
            game=game,
            score=score,
            max_score=100,
            correct_answers=correct,
            total_questions=total,
            time_spent=time_spent,
            xp_earned=xp,
        )
        request.user.add_xp(xp)
        request.user.total_games_played += 1
        request.user.save(update_fields=['total_games_played'])
        new_achievements = check_achievements(request.user)
        return JsonResponse({
            'success': True,
            'score': score,
            'xp_earned': xp,
            'new_level': request.user.level,
            'new_achievements': [{'title': a.title, 'icon': a.icon} for a in new_achievements],
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
