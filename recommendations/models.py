"""
Models for personalized recommendations.
"""
from django.db import models
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class Recommendation(models.Model):
    """Daily personalized recommendations for users."""

    CATEGORY_CHOICES = [
        ('nutrition', 'Питание'),
        ('workout', 'Тренировки'),
        ('lifestyle', 'Образ жизни'),
        ('recovery', 'Восстановление'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations',
                             verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    priority = models.IntegerField(default=0, verbose_name='Приоритет')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'
        ordering = ['-date', '-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date', 'is_read']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date})"

    def save(self, *args, **kwargs):
        logger.info(f"Saving recommendation for user: {self.user.username}")
        super().save(*args, **kwargs)