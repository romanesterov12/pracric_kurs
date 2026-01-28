"""
Service for generating personalized recommendations using rule-based system.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Avg
from tracking.models import FoodLog, ActivityLog, DailyMetrics
from users.models import UserProfile
from .models import Recommendation
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Rule-based recommendation engine."""

    def __init__(self, user):
        self.user = user
        self.today = timezone.now().date()
        self.week_ago = self.today - timedelta(days=7)

    def generate_recommendations(self):
        """Generate all recommendations for the user."""
        recommendations = []

        # Generate different types of recommendations
        recommendations.extend(self._generate_nutrition_recommendations())
        recommendations.extend(self._generate_workout_recommendations())
        recommendations.extend(self._generate_lifestyle_recommendations())
        recommendations.extend(self._generate_recovery_recommendations())

        # Save recommendations to database
        for rec_data in recommendations:
            Recommendation.objects.create(
                user=self.user,
                date=self.today,
                **rec_data
            )

        logger.info(f"Generated {len(recommendations)} recommendations for {self.user.username}")
        return recommendations

    def _get_weekly_nutrition_data(self):
        """Get nutrition data for the past week."""
        food_logs = FoodLog.objects.filter(
            user=self.user,
            date__gte=self.week_ago
        ).values('date').annotate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats')
        )

        return pd.DataFrame(list(food_logs))

    def _get_weekly_activity_data(self):
        """Get activity data for the past week."""
        activity_logs = ActivityLog.objects.filter(
            user=self.user,
            date__gte=self.week_ago
        ).values('date').annotate(
            total_duration=Sum('duration_minutes'),
            total_calories_burned=Sum('calories_burned')
        )

        return pd.DataFrame(list(activity_logs))

    def _generate_nutrition_recommendations(self):
        """Generate nutrition-related recommendations."""
        recommendations = []

        try:
            profile = self.user.profile
            target_calories = profile.daily_calories_target or 2000
        except UserProfile.DoesNotExist:
            return recommendations

        # Get weekly nutrition data
        nutrition_df = self._get_weekly_nutrition_data()

        if nutrition_df.empty:
            recommendations.append({
                'category': 'nutrition',
                'title': 'Начните отслеживать питание',
                'content': 'Регулярное отслеживание питания поможет вам достичь своих целей. Начните с записи завтрака!',
                'priority': 10
            })
            return recommendations

        # Calculate average daily calories
        avg_calories = nutrition_df['total_calories'].mean()

        # Check if calories are too low
        if avg_calories < target_calories * 0.8:
            recommendations.append({
                'category': 'nutrition',
                'title': 'Увеличьте калорийность рациона',
                'content': f'Ваше среднее потребление калорий ({avg_calories:.0f} ккал) ниже целевого ({target_calories} ккал). Добавьте здоровые перекусы между основными приемами пищи.',
                'priority': 9
            })

        # Check if calories are too high
        elif avg_calories > target_calories * 1.2:
            recommendations.append({
                'category': 'nutrition',
                'title': 'Снизьте калорийность рациона',
                'content': f'Ваше среднее потребление калорий ({avg_calories:.0f} ккал) превышает целевое ({target_calories} ккал). Старайтесь контролировать размер порций.',
                'priority': 9
            })

        # Check protein intake
        avg_protein = nutrition_df['total_protein'].mean()
        target_protein = profile.current_weight * 1.6  # 1.6g per kg body weight

        if avg_protein < target_protein * 0.8:
            recommendations.append({
                'category': 'nutrition',
                'title': 'Увеличьте потребление белка',
                'content': f'Ваше среднее потребление белка ({avg_protein:.0f}г) ниже рекомендованного ({target_protein:.0f}г). Добавьте в рацион курицу, рыбу, яйца или бобовые.',
                'priority': 8
            })

        # Hydration reminder
        recommendations.append({
            'category': 'nutrition',
            'title': 'Не забывайте пить воду',
            'content': 'Рекомендуется выпивать 2-3 литра воды в день. Держите бутылку с водой рядом и пейте регулярно в течение дня.',
            'priority': 5
        })

        return recommendations

    def _generate_workout_recommendations(self):
        """Generate workout-related recommendations."""
        recommendations = []

        try:
            profile = self.user.profile
        except UserProfile.DoesNotExist:
            return recommendations

        # Get weekly activity data
        activity_df = self._get_weekly_activity_data()

        if activity_df.empty:
            recommendations.append({
                'category': 'workout',
                'title': 'Начните тренироваться',
                'content': 'Регулярная физическая активность важна для достижения ваших целей. Начните с 20-30 минут легкой активности 3 раза в неделю.',
                'priority': 10
            })
            return recommendations

        # Calculate weekly activity
        days_active = len(activity_df)
        avg_duration = activity_df['total_duration'].mean()

        # Check activity frequency
        if days_active < 3:
            recommendations.append({
                'category': 'workout',
                'title': 'Увеличьте частоту тренировок',
                'content': f'На этой неделе вы тренировались {days_active} дней. Стремитесь к 3-5 тренировкам в неделю для лучших результатов.',
                'priority': 9
            })

        # Check duration
        if avg_duration < 30:
            recommendations.append({
                'category': 'workout',
                'title': 'Увеличьте длительность тренировок',
                'content': f'Средняя длительность ваших тренировок составляет {avg_duration:.0f} минут. Старайтесь тренироваться минимум 30-45 минут.',
                'priority': 7
            })

        # Goal-specific recommendations
        if profile.goal == 'lose_weight':
            recommendations.append({
                'category': 'workout',
                'title': 'Кардио для похудения',
                'content': 'Для эффективного похудения добавьте в свой режим кардио-тренировки: бег, велосипед, плавание или быструю ходьбу 3-4 раза в неделю.',
                'priority': 8
            })
        elif profile.goal == 'gain_muscle':
            recommendations.append({
                'category': 'workout',
                'title': 'Силовые тренировки для набора массы',
                'content': 'Сосредоточьтесь на силовых тренировках с постепенным увеличением веса. Тренируйте каждую группу мышц 2 раза в неделю.',
                'priority': 8
            })

        return recommendations

    def _generate_lifestyle_recommendations(self):
        """Generate lifestyle-related recommendations."""
        recommendations = []

        # Get recent daily metrics
        recent_metrics = DailyMetrics.objects.filter(
            user=self.user,
            date__gte=self.week_ago
        ).aggregate(
            avg_sleep=Avg('sleep_hours'),
            avg_mood=Avg('mood'),
            avg_energy=Avg('energy_level')
        )

        # Sleep recommendations
        avg_sleep = recent_metrics.get('avg_sleep')
        if avg_sleep and avg_sleep < 7:
            recommendations.append({
                'category': 'lifestyle',
                'title': 'Улучшите качество сна',
                'content': f'Ваш средний сон составляет {avg_sleep:.1f} часов. Стремитесь спать 7-9 часов каждую ночь для оптимального восстановления.',
                'priority': 9
            })

        # Mood recommendations
        avg_mood = recent_metrics.get('avg_mood')
        if avg_mood and avg_mood < 3:
            recommendations.append({
                'category': 'lifestyle',
                'title': 'Позаботьтесь о психическом здоровье',
                'content': 'Ваше настроение ниже среднего. Попробуйте медитацию, прогулки на свежем воздухе или общение с близкими людьми.',
                'priority': 8
            })

        # General lifestyle tips
        recommendations.append({
            'category': 'lifestyle',
            'title': 'Соблюдайте режим дня',
            'content': 'Старайтесь ложиться спать и просыпаться в одно и то же время каждый день. Это улучшит качество сна и общее самочувствие.',
            'priority': 6
        })

        return recommendations

    def _generate_recovery_recommendations(self):
        """Generate recovery-related recommendations."""
        recommendations = []

        # Get recent activity
        recent_workouts = ActivityLog.objects.filter(
            user=self.user,
            date__gte=self.week_ago
        ).count()

        if recent_workouts >= 5:
            recommendations.append({
                'category': 'recovery',
                'title': 'Не забывайте про отдых',
                'content': 'Вы активно тренировались на этой неделе. Запланируйте 1-2 дня отдыха для восстановления мышц.',
                'priority': 7
            })

        recommendations.append({
            'category': 'recovery',
            'title': 'Растяжка после тренировок',
            'content': 'Выделяйте 10-15 минут на растяжку после каждой тренировки. Это улучшит гибкость и снизит риск травм.',
            'priority': 6
        })

        return recommendations