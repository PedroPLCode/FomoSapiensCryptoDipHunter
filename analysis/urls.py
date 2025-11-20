"""
URL configuration for the FomoSapiensCryptoDipHunter project.

Defines URL patterns for technical analysis views, including:
- Displaying technical analysis data.
- Updating user settings for technical analysis.
- Refreshing technical analysis data.
- Sending an email report with analysis results.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_technical_analysis, name="show_technical_analysis"),
    path(
        "settings/",
        views.update_technical_analysis_settings,
        name="update_technical_analysis_settings",
    ),
    path("refresh/", views.refresh_technical_analysis, name="refresh_technical_analysis"),
    path("sentiement/", views.refresh_sentiment_analysis, name="refresh_sentiment_analysis"),
    path("gpt/all", views.refresh_gpt_analysis_all_users, name="refresh_gpt_analysis_all_users"),
    path("gpt/selected/", views.refresh_gpt_analysis_selected_user, name="refresh_gpt_analysis_selected_user"),
    path(
        "report/", views.send_email_analysis_report, name="send_email_analysis_report"
    ),
]
