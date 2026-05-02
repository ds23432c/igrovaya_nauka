from django.db import models
from apps.accounts.models import User


class Course(models.Model):
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
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, verbose_name='Категория')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='Уровень')
    cover_url = models.URLField(verbose_name='Обложка')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    xp_reward = models.IntegerField(default=200, verbose_name='Награда XP')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True)

    def lesson_count(self):
        return self.lessons.count()

    def enrolled_count(self):
        return self.enrollments.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    video_url = models.URLField(blank=True, verbose_name='Видео URL')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    xp_reward = models.IntegerField(default=30, verbose_name='Награда XP')

    def __str__(self):
        return f'{self.course.title} — Урок {self.order}: {self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Курс')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
