from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('games/', include('apps.games.urls')),
    path('courses/', include('apps.courses.urls')),
    path('achievements/', include('apps.achievements.urls')),
    path('leaderboard/', include('apps.leaderboard.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
