"""
URL configuration for custom admin app.
"""
from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard_view, name='dashboard'),

    # Users management
    path('users/', views.admin_users_list_view, name='users_list'),
    path('users/<int:pk>/', views.admin_user_detail_view, name='user_detail'),

    # Exercises CRUD
    path('exercises/', views.admin_exercises_list_view, name='exercises_list'),
    path('exercises/create/', views.admin_exercise_create_view, name='exercise_create'),
    path('exercises/<int:pk>/update/', views.admin_exercise_update_view, name='exercise_update'),
    path('exercises/<int:pk>/delete/', views.admin_exercise_delete_view, name='exercise_delete'),

    # Foods CRUD
    path('foods/', views.admin_foods_list_view, name='foods_list'),
    path('foods/create/', views.admin_food_create_view, name='food_create'),
    path('foods/<int:pk>/update/', views.admin_food_update_view, name='food_update'),
    path('foods/<int:pk>/delete/', views.admin_food_delete_view, name='food_delete'),

    # Articles CRUD
    path('articles/', views.admin_articles_list_view, name='articles_list'),
    path('articles/create/', views.admin_article_create_view, name='article_create'),
    path('articles/<int:pk>/update/', views.admin_article_update_view, name='article_update'),
    path('articles/<int:pk>/delete/', views.admin_article_delete_view, name='article_delete'),

    # Statistics
    path('statistics/', views.admin_statistics_view, name='statistics'),
]