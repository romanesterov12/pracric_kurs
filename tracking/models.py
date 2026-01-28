"""
Models for tracking food intake, physical activity, and daily metrics.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class FoodLog(models.Model):
    """Log of food intake."""

    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_logs',
                             verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, verbose_name='Тип приема пищи')
    food_name = models.CharField(max_length=200, verbose_name='Название продукта')
    portion_size = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Размер порции (г)')

    # Nutritional information
    calories = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Калории (ккал)')
    protein = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Белки (г)')
    carbs = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Углеводы (г)')
    fats = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Жиры (г)')

    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        verbose_name = 'Запись о питании'
        verbose_name_plural = 'Записи о питании'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.date})"

    def save(self, *args, **kwargs):
        logger.info(f"Saving food log for user: {self.user.username} - {self.food_name}")
        super().save(*args, **kwargs)


class ActivityLog(models.Model):
    """Log of physical activity."""

    ACTIVITY_TYPE_CHOICES = [
        ('cardio', 'Кардио'),
        ('strength', 'Силовая тренировка'),
        ('flexibility', 'Растяжка/Йога'),
        ('sports', 'Спортивные игры'),
        ('walking', 'Ходьба'),
        ('other', 'Другое'),
    ]

    INTENSITY_CHOICES = [
        ('low', 'Низкая'),
        ('moderate', 'Средняя'),
        ('high', 'Высокая'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs',
                             verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, verbose_name='Тип активности')
    activity_name = models.CharField(max_length=200, verbose_name='Название активности')
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Длительность (мин)')
    intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES, verbose_name='Интенсивность')
    calories_burned = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Сожжено калорий')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        verbose_name = 'Запись о физической активности'
        verbose_name_plural = 'Записи о физической активности'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity_name} ({self.date})"

    def save(self, *args, **kwargs):
        logger.info(f"Saving activity log for user: {self.user.username} - {self.activity_name}")
        super().save(*args, **kwargs)


class DailyMetrics(models.Model):
    """Daily subjective metrics tracking."""

    MOOD_CHOICES = [
        (1, 'Очень плохое'),
        (2, 'Плохое'),
        (3, 'Нормальное'),
        (4, 'Хорошее'),
        (5, 'Отличное'),
    ]

    ENERGY_CHOICES = [
        (1, 'Очень низкая'),
        (2, 'Низкая'),
        (3, 'Средняя'),
        (4, 'Высокая'),
        (5, 'Очень высокая'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='daily_metrics',
                             verbose_name='Пользователь')
    date = models.DateField(unique=True, verbose_name='Дата')
    weight = models.FloatField(
        validators=[MinValueValidator(20), MaxValueValidator(300)],
        null=True,
        blank=True,
        verbose_name='Вес (кг)'
    )
    sleep_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        null=True,
        blank=True,
        verbose_name='Часы сна'
    )
    mood = models.IntegerField(
        choices=MOOD_CHOICES,
        null=True,
        blank=True,
        verbose_name='Настроение'
    )
    energy_level = models.IntegerField(
        choices=ENERGY_CHOICES,
        null=True,
        blank=True,
        verbose_name='Уровень энергии'
    )
    water_intake = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name='Потребление воды (л)'
    )
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Ежедневные показатели'
        verbose_name_plural = 'Ежедневные показатели'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def save(self, *args, **kwargs):
        logger.info(f"Saving daily metrics for user: {self.user.username} - {self.date}")
        super().save(*args, **kwargs)