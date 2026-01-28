"""
URL configuration for tracking app.
"""
from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Food logs
    path('food-logs/', views.food_log_list_view, name='food_log_list'),
    path('food-logs/create/', views.food_log_create_view, name='food_log_create'),
    path('food-logs/<int:pk>/update/', views.food_log_update_view, name='food_log_update'),
    path('food-logs/<int:pk>/delete/', views.food_log_delete_view, name='food_log_delete'),

    # Activity logs
    path('activity-logs/', views.activity_log_list_view, name='activity_log_list'),
    path('activity-logs/create/', views.activity_log_create_view, name='activity_log_create'),
    path('activity-logs/<int:pk>/update/', views.activity_log_update_view, name='activity_log_update'),
    path('activity-logs/<int:pk>/delete/', views.activity_log_delete_view, name='activity_log_delete'),

    # Daily tracking
    path('daily-tracking/', views.daily_tracking_view, name='daily_tracking'),
]