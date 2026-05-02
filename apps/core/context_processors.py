from apps.accounts.models import User
from apps.games.models import Game, GameResult
from apps.courses.models import Course


def site_stats(request):
    return {
        'stat_users': User.objects.count(),
        'stat_games': Game.objects.filter(is_active=True).count(),
        'stat_courses': Course.objects.filter(is_published=True).count(),
        'stat_results': GameResult.objects.count(),
    }
