from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('admin', 'Администратор'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.URLField(blank=True, default='https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200')
    bio = models.TextField(blank=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    total_games_played = models.IntegerField(default=0)
    total_courses_completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_level_title(self):
        titles = {
            1: 'Новичок', 2: 'Исследователь', 3: 'Знаток',
            4: 'Эрудит', 5: 'Мастер', 6: 'Профессор', 7: 'Гений'
        }
        return titles.get(min(self.level, 7), 'Легенда')

    def xp_for_next_level(self):
        return self.level * 500

    def xp_progress_percent(self):
        needed = self.xp_for_next_level()
        current_level_xp = (self.level - 1) * 500
        progress = self.xp - current_level_xp
        return min(int((progress / needed) * 100), 100)

    def add_xp(self, amount):
        self.xp += amount
        new_level = (self.xp // 500) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
