"""
Forms for tracking food, activity, and daily metrics.
"""
from django import forms
from .models import FoodLog, ActivityLog, DailyMetrics


class FoodLogForm(forms.ModelForm):
    """Form for logging food intake."""

    class Meta:
        model = FoodLog
        fields = ['date', 'meal_type', 'food_name', 'portion_size', 'calories', 'protein', 'carbs', 'fats', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название продукта'}),
            'portion_size': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Вес в граммах'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Калории'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Белки (г)'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Углеводы (г)'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Жиры (г)'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Дополнительные заметки'}),
        }


class ActivityLogForm(forms.ModelForm):
    """Form for logging physical activity."""

    class Meta:
        model = ActivityLog
        fields = ['date', 'activity_type', 'activity_name', 'duration_minutes', 'intensity', 'calories_burned', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'activity_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название активности'}),
            'duration_minutes': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Длительность в минутах'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сожжено калорий'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Дополнительные заметки'}),
        }


class DailyMetricsForm(forms.ModelForm):
    """Form for daily metrics tracking."""

    class Meta:
        model = DailyMetrics
        fields = ['date', 'weight', 'sleep_hours', 'mood', 'energy_level', 'water_intake', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Вес (кг)'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'Часы сна'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'energy_level': forms.Select(attrs={'class': 'form-control'}),
            'water_intake': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Литры воды'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Заметки о дне'}),
        }


class FoodSearchForm(forms.Form):
    """Form for searching food items."""

    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск продуктов...',
            'aria-label': 'Поиск'
        })
    )