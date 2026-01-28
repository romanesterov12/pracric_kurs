"""
Forms for user registration, login, and profile management.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})


class UserLoginForm(AuthenticationForm):
    """Form for user login."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DetailedProfileForm(forms.ModelForm):
    """Form for detailed fitness profile."""

    class Meta:
        model = UserProfile
        fields = [
            'height', 'current_weight', 'target_weight', 'goal', 'activity_level',
            'medical_conditions', 'allergies', 'dietary_preferences'
        ]
        widgets = {
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'current_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dietary_preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }