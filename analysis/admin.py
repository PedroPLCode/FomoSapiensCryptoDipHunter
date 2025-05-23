"""
Registers the TechnicalAnalysisSettings model with the Django admin interface.

By registering this model, it allows administrators to manage the settings related to technical analysis
directly from the Django admin panel. The model will be automatically included in the admin interface
with the default options provided by Django unless further customization is done.

This enables users with proper admin privileges to view, add, update, or delete the 'TechnicalAnalysisSettings'
objects through the admin interface.

Model:
    TechnicalAnalysisSettings: A model that stores settings related to technical analysis for the application.
"""

from django.contrib import admin
from .models import TechnicalAnalysisSettings, SentimentAnalysis

admin.site.register(TechnicalAnalysisSettings)


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "sentiment_news_sources",
        "sentiment_news_amount",
        "sentiment_score",
        "sentiment_label",
        "sentiment_last_update_time",
    )
    readonly_fields = ("sentiment_last_update_time",)
    ordering = ("-sentiment_last_update_time",)
