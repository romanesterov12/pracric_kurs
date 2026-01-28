"""
Views for recommendations.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Recommendation
from .services import RecommendationEngine
import logging

logger = logging.getLogger(__name__)


@login_required
def recommendations_view(request):
    """View personalized recommendations."""
    today = timezone.now().date()

    # Check if recommendations exist for today
    today_recommendations = Recommendation.objects.filter(user=request.user, date=today)

    if not today_recommendations.exists():
        # Generate new recommendations
        engine = RecommendationEngine(request.user)
        engine.generate_recommendations()
        messages.info(request, 'Новые рекомендации сгенерированы!')

    # Get all recommendations grouped by category
    recommendations = Recommendation.objects.filter(user=request.user, date=today).order_by('category', '-priority')

    # Group by category
    grouped_recommendations = {}
    for rec in recommendations:
        category = rec.get_category_display()
        if category not in grouped_recommendations:
            grouped_recommendations[category] = []
        grouped_recommendations[category].append(rec)

    context = {
        'grouped_recommendations': grouped_recommendations,
        'today': today,
    }

    return render(request, 'recommendations/recommendations.html', context)


@login_required
def mark_recommendation_read(request, pk):
    """Mark a recommendation as read."""
    if request.method == 'POST':
        try:
            recommendation = Recommendation.objects.get(pk=pk, user=request.user)
            recommendation.is_read = True
            recommendation.save()
            messages.success(request, 'Рекомендация отмечена как прочитанная')
        except Recommendation.DoesNotExist:
            messages.error(request, 'Рекомендация не найдена')

    return redirect('recommendations:recommendations')