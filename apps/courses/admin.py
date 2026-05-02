from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonProgress

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'xp_reward', 'is_published']
    list_filter = ['category', 'level', 'is_published']
    search_fields = ['title']
    inlines = [LessonInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completed', 'enrolled_at']
    list_filter = ['completed']
