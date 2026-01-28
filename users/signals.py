"""
Signals for automatic profile creation.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new CustomUser is created."""
    if created:
        logger.info(f"Creating profile for new user: {instance.username}")
        # Profile will be created when user fills the form
        pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when CustomUser is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
        logger.info(f"Profile saved for user: {instance.username}")