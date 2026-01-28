"""
Models for knowledge base: exercises, foods, and articles.
"""
from django.db import models
from django.core.validators import MinValueValidator
import logging

logger = logging.getLogger(__name__)


class Exercise(models.Model):
    """Exercise database with details and instructions."""

    CATEGORY_CHOICES = [
        ('cardio', 'Кардио'),
        ('strength', 'Силовая'),
        ('flexibility', 'Растяжка'),
        ('sports', 'Спорт'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, verbose_name='Сложность')
    description = models.TextField(verbose_name='Описание')
    instructions = models.TextField(verbose_name='Инструкции')
    calories_per_minute = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Калорий в минуту',
        help_text='Примерное количество калорий, сжигаемых за минуту'
    )
    target_muscles = models.CharField(max_length=200, verbose_name='Целевые мышцы')
    equipment_needed = models.CharField(max_length=200, blank=True, verbose_name='Необходимое оборудование')
    image = models.ImageField(upload_to='exercises/', null=True, blank=True, verbose_name='Изображение')
    video_url = models.URLField(blank=True, verbose_name='Ссылка на видео')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Saving exercise: {self.name}")
        super().save(*args, **kwargs)


class Food(models.Model):
    """Food database with nutritional information."""

    CATEGORY_CHOICES = [
        ('vegetables', 'Овощи'),
        ('fruits', 'Фрукты'),
        ('meat', 'Мясо и птица'),
        ('fish', 'Рыба и морепродукты'),
        ('dairy', 'Молочные продукты'),
        ('grains', 'Крупы и злаки'),
        ('legumes', 'Бобовые'),
        ('nuts', 'Орехи и семена'),
        ('sweets', 'Сладости'),
        ('beverages', 'Напитки'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')

    # Nutritional info per 100g
    calories = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Калории (на 100г)')
    protein = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Белки (г на 100г)')
    carbs = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Углеводы (г на 100г)')
    fats = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Жиры (г на 100г)')
    fiber = models.FloatField(validators=[MinValueValidator(0)], default=0, verbose_name='Клетчатка (г на 100г)')

    description = models.TextField(blank=True, verbose_name='Описание')
    health_benefits = models.TextField(blank=True, verbose_name='Польза для здоровья')
    image = models.ImageField(upload_to='foods/', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Saving food: {self.name}")
        super().save(*args, **kwargs)


class Article(models.Model):
    """Educational articles and tips."""

    CATEGORY_CHOICES = [
        ('nutrition', 'Питание'),
        ('training', 'Тренировки'),
        ('health', 'Здоровье'),
        ('motivation', 'Мотивация'),
        ('lifestyle', 'Образ жизни'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    content = models.TextField(verbose_name='Содержание')
    summary = models.TextField(verbose_name='Краткое описание')
    author = models.CharField(max_length=100, verbose_name='Автор')
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        logger.info(f"Saving article: {self.title}")
        super().save(*args, **kwargs)