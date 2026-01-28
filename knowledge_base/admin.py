from django.contrib import admin
from .models import Exercise, Food, Article


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty', 'calories_per_minute', 'created_at']
    list_filter = ['category', 'difficulty']
    search_fields = ['name', 'description', 'target_muscles']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories', 'protein', 'carbs', 'fats']
    list_filter = ['category']
    search_fields = ['name', 'description']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content', 'author']