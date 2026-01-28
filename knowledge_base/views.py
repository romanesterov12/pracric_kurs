"""
Views for knowledge base browsing.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Exercise, Food, Article


@login_required
def exercises_list_view(request):
    """List all exercises with search and filter."""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')

    exercises = Exercise.objects.all()

    if search_query:
        exercises = exercises.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(target_muscles__icontains=search_query)
        )

    if category:
        exercises = exercises.filter(category=category)

    if difficulty:
        exercises = exercises.filter(difficulty=difficulty)

    paginator = Paginator(exercises, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'difficulty': difficulty,
        'category_choices': Exercise.CATEGORY_CHOICES,
        'difficulty_choices': Exercise.DIFFICULTY_CHOICES,
    }

    return render(request, 'knowledge_base/exercises_list.html', context)


@login_required
def exercise_detail_view(request, pk):
    """View exercise details."""
    exercise = get_object_or_404(Exercise, pk=pk)

    context = {
        'exercise': exercise,
    }

    return render(request, 'knowledge_base/exercise_detail.html', context)


@login_required
def foods_list_view(request):
    """List all foods with search and filter."""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')

    foods = Food.objects.all()

    if search_query:
        foods = foods.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category:
        foods = foods.filter(category=category)

    paginator = Paginator(foods, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'category_choices': Food.CATEGORY_CHOICES,
    }

    return render(request, 'knowledge_base/foods_list.html', context)


@login_required
def food_detail_view(request, pk):
    """View food details."""
    food = get_object_or_404(Food, pk=pk)

    context = {
        'food': food,
    }

    return render(request, 'knowledge_base/food_detail.html', context)


@login_required
def articles_list_view(request):
    """List all published articles."""
    category = request.GET.get('category', '')

    articles = Article.objects.filter(is_published=True)

    if category:
        articles = articles.filter(category=category)

    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
        'category_choices': Article.CATEGORY_CHOICES,
    }

    return render(request, 'knowledge_base/articles_list.html', context)


@login_required
def article_detail_view(request, pk):
    """View article details."""
    article = get_object_or_404(Article, pk=pk, is_published=True)

    context = {
        'article': article,
    }

    return render(request, 'knowledge_base/article_detail.html', context)