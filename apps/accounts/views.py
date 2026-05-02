from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User
from apps.games.models import GameResult
from apps.courses.models import Enrollment
from apps.achievements.models import UserAchievement


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Начни своё путешествие в мир Игровой Науки! 🚀')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.username}! 👋')
            return redirect(request.GET.get('next', 'core:home'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы. До встречи!')
    return redirect('core:home')


@login_required
def profile_view(request):
    user = request.user
    game_results = GameResult.objects.filter(user=user).order_by('-played_at')[:10]
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    return render(request, 'accounts/profile.html', {
        'user': user,
        'game_results': game_results,
        'enrollments': enrollments,
        'user_achievements': user_achievements,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    game_results = GameResult.objects.filter(user=user).order_by('-played_at')[:5]
    return render(request, 'accounts/public_profile.html', {
        'profile_user': user,
        'user_achievements': user_achievements,
        'game_results': game_results,
    })
