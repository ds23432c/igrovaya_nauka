from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/toggle/', views.toggle_user, name='toggle_user'),
    path('games/', views.games_list, name='games'),
    path('games/new/', views.game_edit, name='game_new'),
    path('games/<int:pk>/edit/', views.game_edit, name='game_edit'),
    path('courses/', views.courses_list, name='courses'),
    path('achievements/', views.achievements_list, name='achievements'),
]
