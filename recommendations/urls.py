"""
URL configuration for recommendations app.
"""
from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('recommendations/<int:pk>/read/', views.mark_recommendation_read, name='mark_read'),
]