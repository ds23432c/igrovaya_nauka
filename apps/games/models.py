from django.db import models
from apps.accounts.models import User


class Game(models.Model):
    CATEGORY_CHOICES = [
        ('math', 'Математика'),
        ('physics', 'Физика'),
        ('chemistry', 'Химия'),
        ('biology', 'Биология'),
        ('geography', 'География'),
        ('history', 'История'),
        ('logic', 'Логика'),
        ('language', 'Русский язык'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Лёгкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    TYPE_CHOICES = [
        ('quiz', 'Викторина'),
        ('puzzle', 'Головоломка'),
        ('memory', 'Память'),
        ('typing', 'Набор текста'),
        ('math_race', 'Математическая гонка'),
        ('word', 'Слова'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, verbose_name='Категория')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium', verbose_name='Сложность')
    game_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Тип игры')
    cover_url = models.URLField(verbose_name='Обложка')
    xp_reward = models.IntegerField(default=50, verbose_name='Награда XP')
    play_time = models.IntegerField(default=5, verbose_name='Время (мин)')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    plays_count = models.IntegerField(default=0, verbose_name='Сыграно раз')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-created_at']


class Question(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='questions', verbose_name='Игра')
    text = models.TextField(verbose_name='Вопрос')
    option_a = models.CharField(max_length=300, verbose_name='Вариант А')
    option_b = models.CharField(max_length=300, verbose_name='Вариант Б')
    option_c = models.CharField(max_length=300, verbose_name='Вариант В')
    option_d = models.CharField(max_length=300, verbose_name='Вариант Г')
    correct = models.CharField(max_length=1, choices=[('a','А'),('b','Б'),('c','В'),('d','Г')], verbose_name='Правильный ответ')
    explanation = models.TextField(blank=True, verbose_name='Объяснение')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.game.title} — {self.text[:50]}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']


class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_results', verbose_name='Пользователь')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='results', verbose_name='Игра')
    score = models.IntegerField(default=0, verbose_name='Очки')
    max_score = models.IntegerField(default=100, verbose_name='Макс. очки')
    correct_answers = models.IntegerField(default=0, verbose_name='Правильных ответов')
    total_questions = models.IntegerField(default=0, verbose_name='Всего вопросов')
    time_spent = models.IntegerField(default=0, verbose_name='Время (сек)')
    xp_earned = models.IntegerField(default=0, verbose_name='XP получено')
    played_at = models.DateTimeField(auto_now_add=True, verbose_name='Сыграно')

    def percent(self):
        if self.total_questions == 0:
            return 0
        return int((self.correct_answers / self.total_questions) * 100)

    def __str__(self):
        return f'{self.user.username} — {self.game.title} — {self.score}'

    class Meta:
        verbose_name = 'Результат игры'
        verbose_name_plural = 'Результаты игр'
        ordering = ['-played_at']
