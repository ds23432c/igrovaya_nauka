from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Course, Lesson, Enrollment, LessonProgress
from apps.achievements.utils import check_achievements


def courses_list(request):
    category = request.GET.get('category', '')
    level = request.GET.get('level', '')
    courses = Course.objects.filter(is_published=True)
    if category:
        courses = courses.filter(category=category)
    if level:
        courses = courses.filter(level=level)
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': Course.CATEGORY_CHOICES,
        'levels': Course.LEVEL_CHOICES,
        'selected_category': category,
        'selected_level': level,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, is_published=True)
    is_enrolled = False
    enrollment = None
    completed_lessons = []
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
            completed_lessons = LessonProgress.objects.filter(
                user=request.user, lesson__course=course, completed=True
            ).values_list('lesson_id', flat=True)
        except Enrollment.DoesNotExist:
            pass
    lessons = course.lessons.all()
    return render(request, 'courses/detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'completed_lessons': list(completed_lessons),
    })


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f'Вы записались на курс «{course.title}»! 🎉')
    return redirect('courses:detail', pk=pk)


@login_required
def lesson_view(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    if request.method == 'POST':
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
            request.user.add_xp(lesson.xp_reward)
            messages.success(request, f'+{lesson.xp_reward} XP! Урок завершён! ⭐')

            total = course.lessons.count()
            done = LessonProgress.objects.filter(user=request.user, lesson__course=course, completed=True).count()
            if done >= total and not enrollment.completed:
                enrollment.completed = True
                enrollment.completed_at = timezone.now()
                enrollment.save()
                request.user.add_xp(course.xp_reward)
                request.user.total_courses_completed += 1
                request.user.save(update_fields=['total_courses_completed'])
                check_achievements(request.user)
                messages.success(request, f'🏆 Курс «{course.title}» пройден! +{course.xp_reward} XP!')
        return redirect('courses:lesson', course_pk=course_pk, lesson_pk=lesson_pk)

    all_lessons = list(course.lessons.all())
    current_index = next((i for i, l in enumerate(all_lessons) if l.pk == lesson.pk), 0)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
    })
