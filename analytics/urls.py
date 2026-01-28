"""
URL configuration for analytics app.
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('analytics/', views.analytics_view, name='analytics'),
    path('analytics/export/xlsx/', views.export_xlsx_view, name='export_xlsx'),
    path('analytics/export/pdf/', views.export_pdf_view, name='export_pdf'),
]