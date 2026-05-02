from django.shortcuts import render
from apps.accounts.models import User


def leaderboard_view(request):
    top_users = User.objects.filter(is_active=True).order_by('-xp')[:50]
    my_rank = None
    if request.user.is_authenticated:
        my_rank = User.objects.filter(xp__gt=request.user.xp).count() + 1
    return render(request, 'leaderboard/list.html', {
        'top_users': top_users,
        'my_rank': my_rank,
    })
