"""
Views for custom admin panel.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser, UserProfile
from tracking.models import FoodLog, ActivityLog, DailyMetrics
from knowledge_base.models import Exercise, Food, Article
from knowledge_base.forms import ExerciseForm, FoodForm, ArticleForm
from recommendations.models import Recommendation
import logging

logger = logging.getLogger(__name__)


@staff_member_required
def admin_dashboard_view(request):
    """Main admin dashboard with platform statistics."""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # User statistics
    total_users = CustomUser.objects.count()
    new_users_week = CustomUser.objects.filter(date_joined__gte=week_ago).count()
    active_users_week = FoodLog.objects.filter(created_at__gte=week_ago).values('user').distinct().count()

    # Content statistics
    total_exercises = Exercise.objects.count()
    total_foods = Food.objects.count()
    total_articles = Article.objects.count()

    # Activity statistics
    total_food_logs = FoodLog.objects.filter(created_at__gte=month_ago).count()
    total_activity_logs = ActivityLog.objects.filter(created_at__gte=month_ago).count()
    total_recommendations = Recommendation.objects.filter(date__gte=month_ago).count()

    # User engagement
    avg_logs_per_user = FoodLog.objects.filter(created_at__gte=month_ago).values('user').annotate(
        count=Count('id')
    ).aggregate(avg=Avg('count'))['avg'] or 0

    # Popular exercises and foods
    popular_exercises = Exercise.objects.annotate(
        usage_count=Count('activitylog')
    ).order_by('-usage_count')[:5]

    popular_foods = Food.objects.all()[:5]  # You can add usage tracking

    context = {
        'total_users': total_users,
        'new_users_week': new_users_week,
        'active_users_week': active_users_week,
        'total_exercises': total_exercises,
        'total_foods': total_foods,
        'total_articles': total_articles,
        'total_food_logs': total_food_logs,
        'total_activity_logs': total_activity_logs,
        'total_recommendations': total_recommendations,
        'avg_logs_per_user': round(avg_logs_per_user, 1),
        'popular_exercises': popular_exercises,
        'popular_foods': popular_foods,
    }

    return render(request, 'custom_admin/dashboard.html', context)


@staff_member_required
def admin_users_list_view(request):
    """List all users with search and filter."""
    search_query = request.GET.get('search', '')

    users = CustomUser.objects.all().select_related('profile')

    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query)

    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'custom_admin/users_list.html', context)


@staff_member_required
def admin_user_detail_view(request, pk):
    """View user details and statistics."""
    user = get_object_or_404(CustomUser, pk=pk)

    # User statistics
    total_food_logs = FoodLog.objects.filter(user=user).count()
    total_activity_logs = ActivityLog.objects.filter(user=user).count()
    total_days_tracked = DailyMetrics.objects.filter(user=user).count()

    # Recent activity
    recent_food_logs = FoodLog.objects.filter(user=user).order_by('-created_at')[:5]
    recent_activity_logs = ActivityLog.objects.filter(user=user).order_by('-created_at')[:5]

    context = {
        'user_obj': user,
        'total_food_logs': total_food_logs,
        'total_activity_logs': total_activity_logs,
        'total_days_tracked': total_days_tracked,
        'recent_food_logs': recent_food_logs,
        'recent_activity_logs': recent_activity_logs,
    }

    return render(request, 'custom_admin/user_detail.html', context)


@staff_member_required
def admin_exercises_list_view(request):
    """List and manage exercises."""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')

    exercises = Exercise.objects.all()

    if search_query:
        exercises = exercises.filter(name__icontains=search_query)

    if category:
        exercises = exercises.filter(category=category)

    paginator = Paginator(exercises, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'category_choices': Exercise.CATEGORY_CHOICES,
    }

    return render(request, 'custom_admin/exercises_crud.html', context)


@staff_member_required
def admin_exercise_create_view(request):
    """Create a new exercise."""
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info(f"Exercise created by admin: {request.user.username}")
            messages.success(request, 'Упражнение успешно создано!')
            return redirect('custom_admin:exercises_list')
    else:
        form = ExerciseForm()

    return render(request, 'custom_admin/exercise_form.html', {'form': form, 'action': 'Создать'})


@staff_member_required
def admin_exercise_update_view(request, pk):
    """Update an exercise."""
    exercise = get_object_or_404(Exercise, pk=pk)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)
        if form.is_valid():
            form.save()
            logger.info(f"Exercise updated by admin: {request.user.username}")
            messages.success(request, 'Упражнение успешно обновлено!')
            return redirect('custom_admin:exercises_list')
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'custom_admin/exercise_form.html', {'form': form, 'action': 'Редактировать'})


@staff_member_required
def admin_exercise_delete_view(request, pk):
    """Delete an exercise."""
    exercise = get_object_or_404(Exercise, pk=pk)

    if request.method == 'POST':
        exercise.delete()
        logger.info(f"Exercise deleted by admin: {request.user.username}")
        messages.success(request, 'Упражнение успешно удалено!')
        return redirect('custom_admin:exercises_list')

    return render(request, 'custom_admin/exercise_confirm_delete.html', {'exercise': exercise})


@staff_member_required
def admin_foods_list_view(request):
    """List and manage foods."""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')

    foods = Food.objects.all()

    if search_query:
        foods = foods.filter(name__icontains=search_query)

    if category:
        foods = foods.filter(category=category)

    paginator = Paginator(foods, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'category_choices': Food.CATEGORY_CHOICES,
    }

    return render(request, 'custom_admin/foods_crud.html', context)


@staff_member_required
def admin_food_create_view(request):
    """Create a new food."""
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info(f"Food created by admin: {request.user.username}")
            messages.success(request, 'Продукт успешно создан!')
            return redirect('custom_admin:foods_list')
    else:
        form = FoodForm()

    return render(request, 'custom_admin/food_form.html', {'form': form, 'action': 'Создать'})


@staff_member_required
def admin_food_update_view(request, pk):
    """Update a food."""
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            logger.info(f"Food updated by admin: {request.user.username}")
            messages.success(request, 'Продукт успешно обновлен!')
            return redirect('custom_admin:foods_list')
    else:
        form = FoodForm(instance=food)

    return render(request, 'custom_admin/food_form.html', {'form': form, 'action': 'Редактировать'})


@staff_member_required
def admin_food_delete_view(request, pk):
    """Delete a food."""
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        food.delete()
        logger.info(f"Food deleted by admin: {request.user.username}")
        messages.success(request, 'Продукт успешно удален!')
        return redirect('custom_admin:foods_list')

    return render(request, 'custom_admin/food_confirm_delete.html', {'food': food})


@staff_member_required
def admin_articles_list_view(request):
    """List and manage articles."""
    articles = Article.objects.all()

    paginator = Paginator(articles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'custom_admin/articles_crud.html', context)


@staff_member_required
def admin_article_create_view(request):
    """Create a new article."""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info(f"Article created by admin: {request.user.username}")
            messages.success(request, 'Статья успешно создана!')
            return redirect('custom_admin:articles_list')
    else:
        form = ArticleForm()

    return render(request, 'custom_admin/article_form.html', {'form': form, 'action': 'Создать'})


@staff_member_required
def admin_article_update_view(request, pk):
    """Update an article."""
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            logger.info(f"Article updated by admin: {request.user.username}")
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('custom_admin:articles_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'custom_admin/article_form.html', {'form': form, 'action': 'Редактировать'})


@staff_member_required
def admin_article_delete_view(request, pk):
    """Delete an article."""
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        article.delete()
        logger.info(f"Article deleted by admin: {request.user.username}")
        messages.success(request, 'Статья успешно удалена!')
        return redirect('custom_admin:articles_list')

    return render(request, 'custom_admin/article_confirm_delete.html', {'article': article})


@staff_member_required
def admin_statistics_view(request):
    """View platform statistics and analytics."""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # User activity over time
    user_registrations = []
    for i in range(30):
        date = today - timedelta(days=29 - i)
        count = CustomUser.objects.filter(date_joined__date=date).count()
        user_registrations.append({
            'date': date.isoformat(),
            'count': count
        })

    # Content usage
    food_logs_per_day = []
    activity_logs_per_day = []
    for i in range(30):
        date = today - timedelta(days=29 - i)
        food_count = FoodLog.objects.filter(date=date).count()
        activity_count = ActivityLog.objects.filter(date=date).count()
        food_logs_per_day.append({'date': date.isoformat(), 'count': food_count})
        activity_logs_per_day.append({'date': date.isoformat(), 'count': activity_count})

    # User engagement metrics
    total_users = CustomUser.objects.count()
    active_users = FoodLog.objects.filter(created_at__gte=week_ago).values('user').distinct().count()
    engagement_rate = (active_users / total_users * 100) if total_users > 0 else 0

    import json
    context = {
        'user_registrations': json.dumps(user_registrations),
        'food_logs_per_day': json.dumps(food_logs_per_day),
        'activity_logs_per_day': json.dumps(activity_logs_per_day),
        'total_users': total_users,
        'active_users': active_users,
        'engagement_rate': round(engagement_rate, 1),
    }

    return render(request, 'custom_admin/statistics.html', context)