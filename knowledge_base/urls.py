"""
URL configuration for knowledge base app.
"""
from django.urls import path
from . import views

app_name = 'knowledge_base'

urlpatterns = [
    # Exercises
    path('exercises/', views.exercises_list_view, name='exercises_list'),
    path('exercises/<int:pk>/', views.exercise_detail_view, name='exercise_detail'),

    # Foods
    path('foods/', views.foods_list_view, name='foods_list'),
    path('foods/<int:pk>/', views.food_detail_view, name='food_detail'),

    # Articles
    path('articles/', views.articles_list_view, name='articles_list'),
    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
]