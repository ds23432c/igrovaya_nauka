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
    path('courses/new/', views.course_edit, name='course_new'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('achievements/', views.achievements_list, name='achievements'),
    path('achievements/new/', views.achievement_edit, name='achievement_new'),
    path('achievements/<int:pk>/edit/', views.achievement_edit, name='achievement_edit'),
]
