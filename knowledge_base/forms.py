"""
Forms for knowledge base management.
"""
from django import forms
from .models import Exercise, Food, Article


class ExerciseForm(forms.ModelForm):
    """Form for creating/editing exercises."""

    class Meta:
        model = Exercise
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'calories_per_minute': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'target_muscles': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_needed': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class FoodForm(forms.ModelForm):
    """Form for creating/editing foods."""

    class Meta:
        model = Food
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fiber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'health_benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ArticleForm(forms.ModelForm):
    """Form for creating/editing articles."""

    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }