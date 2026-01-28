"""
URL configuration for FitTracker project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin (disabled in favor of custom admin)
    path('django-admin/', admin.site.urls),

    # Redirect root to dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),

    # App URLs
    path('', include('users.urls')),
    path('', include('tracking.urls')),
    path('', include('recommendations.urls')),
    path('', include('analytics.urls')),
    path('', include('knowledge_base.urls')),
    path('admin/', include('custom_admin.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)