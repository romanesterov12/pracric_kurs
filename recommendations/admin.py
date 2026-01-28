from django.contrib import admin
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'date', 'priority', 'is_read']
    list_filter = ['category', 'date', 'is_read']
    search_fields = ['user__username', 'title', 'content']
    date_hierarchy = 'date'