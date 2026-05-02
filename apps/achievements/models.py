from django.db import models
from apps.accounts.models import User


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('games', 'Игры'),
        ('courses', 'Курсы'),
        ('xp', 'Опыт'),
        ('social', 'Социальное'),
        ('special', 'Особое'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon = models.CharField(max_length=10, default='🏆', verbose_name='Иконка')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='special', verbose_name='Категория')
    condition_type = models.CharField(max_length=50, verbose_name='Тип условия')
    condition_value = models.IntegerField(default=1, verbose_name='Значение условия')
    xp_reward = models.IntegerField(default=100, verbose_name='Награда XP')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements', verbose_name='Пользователь')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, verbose_name='Достижение')
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='Получено')

    class Meta:
        unique_together = ['user', 'achievement']
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
