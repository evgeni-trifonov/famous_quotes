from django.contrib import admin
from .models import Quote, SiteStats

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'source', 'weight', 'likes', 'dislikes', 'views']
    list_editable = ['weight']  # Позволяет редактировать вес прямо в списке
    list_filter = ['source']
    search_fields = ['text', 'source']
    fieldsets = [
        (None, {
            'fields': ['text', 'source', 'weight']
        }),
        ('Статистика', {
            'fields': ['likes', 'dislikes', 'views'],
            'classes': ['collapse']  # Сворачиваемый блок
        }),
    ]

@admin.register(SiteStats)
class SiteStatsAdmin(admin.ModelAdmin):
    list_display = ['total_views', 'last_updated']
    readonly_fields = ['total_views', 'last_updated']
