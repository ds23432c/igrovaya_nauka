from django.shortcuts import render
from .models import Achievement, UserAchievement
from django.contrib.auth.decorators import login_required


def achievements_list(request):
    achievements = Achievement.objects.filter(is_active=True)
    earned_ids = []
    if request.user.is_authenticated:
        earned_ids = UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
    return render(request, 'achievements/list.html', {
        'achievements': achievements,
        'earned_ids': list(earned_ids),
    })
