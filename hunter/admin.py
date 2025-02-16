"""
Registers the TechnicalAnalysisHunter model with the Django admin interface.

By registering this model, it allows administrators to manage the settings related to hunter
directly from the Django admin panel. The model will be automatically included in the admin interface 
with the default options provided by Django unless further customization is done.

This enables users with proper admin privileges to view, add, update, or delete the 'TechnicalAnalysisHunter' 
objects through the admin interface.

Model:
    TechnicalAnalysisHunter: A model that stores settings related to technical analysis hunter for the application.
"""
from django.contrib import admin
from .models import TechnicalAnalysisHunter

admin.site.register(TechnicalAnalysisHunter)