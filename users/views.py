"""
Views for user authentication and profile management.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, DetailedProfileForm
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('tracking:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered: {user.username}")
            messages.success(request, 'Регистрация прошла успешно! Заполните свой профиль.')
            return redirect('users:profile_edit')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('tracking:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User logged in: {username}")
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('tracking:dashboard')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    username = request.user.username
    logout(request)
    logger.info(f"User logged out: {username}")
    messages.info(request, 'Вы вышли из системы.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """View user profile."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_edit_view(request):
    """Edit user profile."""
    # Get or create profile
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = DetailedProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            logger.info(f"Profile updated for user: {request.user.username}")
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = DetailedProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile_edit.html', context)