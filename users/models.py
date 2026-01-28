"""
User models for authentication and profile management.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import logging

logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    """
    Extended user model with additional fields for fitness tracking.
    """
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Пол')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        logger.info(f"Saving user: {self.username}")
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    Detailed user profile with anthropometric data and fitness goals.
    """
    GOAL_CHOICES = [
        ('lose_weight', 'Похудение'),
        ('gain_muscle', 'Набор массы'),
        ('maintain', 'Поддержание формы'),
        ('endurance', 'Развитие выносливости'),
        ('strength', 'Развитие силы'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Сидячий образ жизни'),
        ('light', 'Легкая активность (1-3 дня в неделю)'),
        ('moderate', 'Умеренная активность (3-5 дней в неделю)'),
        ('high', 'Высокая активность (6-7 дней в неделю)'),
        ('extreme', 'Экстремальная активность (2 раза в день)'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile',
                                verbose_name='Пользователь')

    # Anthropometric data
    height = models.FloatField(
        validators=[MinValueValidator(50), MaxValueValidator(250)],
        verbose_name='Рост (см)',
        help_text='Рост в сантиметрах'
    )
    current_weight = models.FloatField(
        validators=[MinValueValidator(20), MaxValueValidator(300)],
        verbose_name='Текущий вес (кг)'
    )
    target_weight = models.FloatField(
        validators=[MinValueValidator(20), MaxValueValidator(300)],
        verbose_name='Целевой вес (кг)'
    )

    # Goals and preferences
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, verbose_name='Цель')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, verbose_name='Уровень активности')

    # Medical and dietary information
    medical_conditions = models.TextField(blank=True, verbose_name='Медицинские ограничения')
    allergies = models.TextField(blank=True, verbose_name='Аллергии')
    dietary_preferences = models.TextField(blank=True, verbose_name='Пищевые предпочтения')

    # Calculated fields
    bmi = models.FloatField(null=True, blank=True, verbose_name='ИМТ')
    daily_calories_target = models.IntegerField(null=True, blank=True, verbose_name='Целевая калорийность (ккал/день)')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль {self.user.username}"

    def calculate_bmi(self):
        """Calculate Body Mass Index."""
        if self.height and self.current_weight:
            height_m = self.height / 100
            self.bmi = round(self.current_weight / (height_m ** 2), 2)
        return self.bmi

    def calculate_daily_calories(self):
        """
        Calculate daily calorie target using Mifflin-St Jeor Equation.
        """
        if not all([self.user.date_of_birth, self.current_weight, self.height, self.user.gender]):
            return None

        from datetime import date
        age = (date.today() - self.user.date_of_birth).days // 365

        # Calculate BMR (Basal Metabolic Rate)
        if self.user.gender == 'M':
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * age + 5
        else:
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * age - 161

        # Activity multiplier
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'high': 1.725,
            'extreme': 1.9,
        }

        tdee = bmr * activity_multipliers.get(self.activity_level, 1.2)

        # Adjust based on goal
        if self.goal == 'lose_weight':
            self.daily_calories_target = int(tdee - 500)  # 500 calorie deficit
        elif self.goal == 'gain_muscle':
            self.daily_calories_target = int(tdee + 300)  # 300 calorie surplus
        else:
            self.daily_calories_target = int(tdee)

        return self.daily_calories_target

    def save(self, *args, **kwargs):
        """Override save to calculate BMI and calories."""
        self.calculate_bmi()
        self.calculate_daily_calories()
        logger.info(f"Saving profile for user: {self.user.username}")
        super().save(*args, **kwargs)