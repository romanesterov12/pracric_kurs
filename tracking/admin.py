from django.contrib import admin
from .models import FoodLog, ActivityLog, DailyMetrics


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_name', 'meal_type', 'date', 'calories', 'created_at']
    list_filter = ['meal_type', 'date', 'created_at']
    search_fields = ['user__username', 'food_name']
    date_hierarchy = 'date'


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_name', 'activity_type', 'date', 'duration_minutes', 'calories_burned']
    list_filter = ['activity_type', 'intensity', 'date']
    search_fields = ['user__username', 'activity_name']
    date_hierarchy = 'date'


@admin.register(DailyMetrics)
class DailyMetricsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'sleep_hours', 'mood', 'energy_level']
    list_filter = ['date', 'mood', 'energy_level']
    search_fields = ['user__username']
    date_hierarchy = 'date'