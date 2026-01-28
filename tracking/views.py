"""
Views for tracking dashboard, food logs, activity logs, and daily metrics.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FoodLog, ActivityLog, DailyMetrics
from .forms import FoodLogForm, ActivityLogForm, DailyMetricsForm, FoodSearchForm
from knowledge_base.models import Food
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard_view(request):
    """Main dashboard with overview of today's tracking."""
    today = timezone.now().date()

    # Get today's data
    food_logs = FoodLog.objects.filter(user=request.user, date=today)
    activity_logs = ActivityLog.objects.filter(user=request.user, date=today)

    try:
        daily_metrics = DailyMetrics.objects.get(user=request.user, date=today)
    except DailyMetrics.DoesNotExist:
        daily_metrics = None

    # Calculate totals
    total_calories_consumed = food_logs.aggregate(total=Sum('calories'))['total'] or 0
    total_protein = food_logs.aggregate(total=Sum('protein'))['total'] or 0
    total_carbs = food_logs.aggregate(total=Sum('carbs'))['total'] or 0
    total_fats = food_logs.aggregate(total=Sum('fats'))['total'] or 0
    total_calories_burned = activity_logs.aggregate(total=Sum('calories_burned'))['total'] or 0

    # Get user's calorie target
    calorie_target = 2000  # Default
    if hasattr(request.user, 'profile') and request.user.profile.daily_calories_target:
        calorie_target = request.user.profile.daily_calories_target

    # Calculate net calories
    net_calories = total_calories_consumed - total_calories_burned
    calorie_progress = (net_calories / calorie_target * 100) if calorie_target > 0 else 0

    # Get last 7 days weight data for chart
    week_ago = today - timedelta(days=7)
    weight_data = DailyMetrics.objects.filter(
        user=request.user,
        date__gte=week_ago,
        weight__isnull=False
    ).order_by('date').values('date', 'weight')

    context = {
        'today': today,
        'food_logs': food_logs[:5],
        'activity_logs': activity_logs[:5],
        'daily_metrics': daily_metrics,
        'total_calories_consumed': total_calories_consumed,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
        'total_calories_burned': total_calories_burned,
        'net_calories': net_calories,
        'calorie_target': calorie_target,
        'calorie_progress': min(calorie_progress, 100),
        'weight_data': list(weight_data),
    }

    return render(request, 'tracking/dashboard.html', context)


@login_required
def food_log_list_view(request):
    """List all food logs with search, filter, and pagination."""
    # Get query parameters
    search_query = request.GET.get('search', '')
    meal_type = request.GET.get('meal_type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', '-date')

    # Base queryset
    food_logs = FoodLog.objects.filter(user=request.user).select_related('user')

    # Apply search filter
    if search_query:
        food_logs = food_logs.filter(
            Q(food_name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Apply meal type filter
    if meal_type:
        food_logs = food_logs.filter(meal_type=meal_type)

    # Apply date filters
    if date_from:
        food_logs = food_logs.filter(date__gte=date_from)
    if date_to:
        food_logs = food_logs.filter(date__lte=date_to)

    # Apply sorting
    valid_sort_fields = ['date', '-date', 'calories', '-calories', 'food_name', '-food_name']
    if sort_by in valid_sort_fields:
        food_logs = food_logs.order_by(sort_by)

    # Pagination
    paginator = Paginator(food_logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'meal_type': meal_type,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'meal_choices': FoodLog.MEAL_TYPE_CHOICES,
    }

    return render(request, 'tracking/food_log.html', context)


@login_required
def food_log_create_view(request):
    """Create a new food log entry."""
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = request.user
            food_log.save()
            logger.info(f"Food log created by {request.user.username}")
            messages.success(request, 'Запись о питании добавлена!')
            return redirect('tracking:food_log_list')
    else:
        # Pre-fill with today's date
        initial_data = {'date': timezone.now().date()}
        form = FoodLogForm(initial=initial_data)

    return render(request, 'tracking/food_log_form.html', {'form': form, 'action': 'Добавить'})


@login_required
def food_log_update_view(request, pk):
    """Update an existing food log entry."""
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)

    if request.method == 'POST':
        form = FoodLogForm(request.POST, instance=food_log)
        if form.is_valid():
            form.save()
            logger.info(f"Food log updated by {request.user.username}")
            messages.success(request, 'Запись о питании обновлена!')
            return redirect('tracking:food_log_list')
    else:
        form = FoodLogForm(instance=food_log)

    return render(request, 'tracking/food_log_form.html', {'form': form, 'action': 'Редактировать'})


@login_required
def food_log_delete_view(request, pk):
    """Delete a food log entry."""
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)

    if request.method == 'POST':
        food_log.delete()
        logger.info(f"Food log deleted by {request.user.username}")
        messages.success(request, 'Запись о питании удалена!')
        return redirect('tracking:food_log_list')

    return render(request, 'tracking/food_log_confirm_delete.html', {'food_log': food_log})


@login_required
def activity_log_list_view(request):
    """List all activity logs with search, filter, and pagination."""
    # Get query parameters
    search_query = request.GET.get('search', '')
    activity_type = request.GET.get('activity_type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', '-date')

    # Base queryset
    activity_logs = ActivityLog.objects.filter(user=request.user).select_related('user')

    # Apply search filter
    if search_query:
        activity_logs = activity_logs.filter(
            Q(activity_name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Apply activity type filter
    if activity_type:
        activity_logs = activity_logs.filter(activity_type=activity_type)

    # Apply date filters
    if date_from:
        activity_logs = activity_logs.filter(date__gte=date_from)
    if date_to:
        activity_logs = activity_logs.filter(date__lte=date_to)

    # Apply sorting
    valid_sort_fields = ['date', '-date', 'calories_burned', '-calories_burned', 'duration_minutes',
                         '-duration_minutes']
    if sort_by in valid_sort_fields:
        activity_logs = activity_logs.order_by(sort_by)

    # Pagination
    paginator = Paginator(activity_logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'activity_type': activity_type,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'activity_choices': ActivityLog.ACTIVITY_TYPE_CHOICES,
    }

    return render(request, 'tracking/activity_log.html', context)


@login_required
def activity_log_create_view(request):
    """Create a new activity log entry."""
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            activity_log = form.save(commit=False)
            activity_log.user = request.user
            activity_log.save()
            logger.info(f"Activity log created by {request.user.username}")
            messages.success(request, 'Запись о физической активности добавлена!')
            return redirect('tracking:activity_log_list')
    else:
        initial_data = {'date': timezone.now().date()}
        form = ActivityLogForm(initial=initial_data)

    return render(request, 'tracking/activity_log_form.html', {'form': form, 'action': 'Добавить'})


@login_required
def activity_log_update_view(request, pk):
    """Update an existing activity log entry."""
    activity_log = get_object_or_404(ActivityLog, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ActivityLogForm(request.POST, instance=activity_log)
        if form.is_valid():
            form.save()
            logger.info(f"Activity log updated by {request.user.username}")
            messages.success(request, 'Запись о физической активности обновлена!')
            return redirect('tracking:activity_log_list')
    else:
        form = ActivityLogForm(instance=activity_log)

    return render(request, 'tracking/activity_log_form.html', {'form': form, 'action': 'Редактировать'})


@login_required
def activity_log_delete_view(request, pk):
    """Delete an activity log entry."""
    activity_log = get_object_or_404(ActivityLog, pk=pk, user=request.user)

    if request.method == 'POST':
        activity_log.delete()
        logger.info(f"Activity log deleted by {request.user.username}")
        messages.success(request, 'Запись о физической активности удалена!')
        return redirect('tracking:activity_log_list')

    return render(request, 'tracking/activity_log_confirm_delete.html', {'activity_log': activity_log})


@login_required
def daily_tracking_view(request):
    """View for comprehensive daily tracking."""
    today = timezone.now().date()

    # Get or create daily metrics
    daily_metrics, created = DailyMetrics.objects.get_or_create(
        user=request.user,
        date=today
    )

    if request.method == 'POST':
        form = DailyMetricsForm(request.POST, instance=daily_metrics)
        if form.is_valid():
            form.save()
            logger.info(f"Daily metrics updated by {request.user.username}")
            messages.success(request, 'Ежедневные показатели обновлены!')
            return redirect('tracking:dashboard')
    else:
        form = DailyMetricsForm(instance=daily_metrics)

    context = {
        'form': form,
        'today': today,
    }

    return render(request, 'tracking/daily_tracking.html', context)