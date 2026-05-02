from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses_list, name='list'),
    path('<int:pk>/', views.course_detail, name='detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll'),
    path('<int:course_pk>/lesson/<int:lesson_pk>/', views.lesson_view, name='lesson'),
]
