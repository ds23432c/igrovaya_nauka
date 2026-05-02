from .models import Achievement, UserAchievement


def check_achievements(user):
    new_achievements = []
    all_achievements = Achievement.objects.filter(is_active=True)
    earned_ids = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)

    for ach in all_achievements:
        if ach.id in earned_ids:
            continue
        earned = False
        if ach.condition_type == 'games_played' and user.total_games_played >= ach.condition_value:
            earned = True
        elif ach.condition_type == 'courses_completed' and user.total_courses_completed >= ach.condition_value:
            earned = True
        elif ach.condition_type == 'xp_reached' and user.xp >= ach.condition_value:
            earned = True
        elif ach.condition_type == 'level_reached' and user.level >= ach.condition_value:
            earned = True

        if earned:
            UserAchievement.objects.create(user=user, achievement=ach)
            user.add_xp(ach.xp_reward)
            new_achievements.append(ach)

    return new_achievements
