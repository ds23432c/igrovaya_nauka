from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'level', 'xp', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'level']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
