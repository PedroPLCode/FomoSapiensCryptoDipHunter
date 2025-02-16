"""
URL patterns for the 'hunter' app in the project.

This file maps URLs to views for handling the hunter-related functionality:
- Viewing the list of hunters
- Creating or editing hunters
- Deleting a specific hunter
- Removing all hunters
- Starting or stopping specific hunters or all hunters

Each view is protected by login_required and exception handling to ensure proper access control and error management.

URL patterns:
- 'hunter_list': Displays all hunters for the current user.
- 'hunter_create_or_edit': Allows creating or editing a hunter.
- 'hunter_delete': Deletes a specific hunter.
- 'remove_all_hunters': Removes all hunters for the current user.
- 'start_all_hunters': Starts all hunters for the current user.
- 'start_hunter': Starts a specific hunter.
- 'stop_hunter': Stops a specific hunter.
- 'stop_all_hunters': Stops all hunters for the current user.
"""
from django.urls import path
from . import views

app_name = 'hunter'

urlpatterns = [
    path('', views.hunter_list, name='hunter_list'),
    path('create_edit/<int:pk>/', views.hunter_create_or_edit, name='hunter_create_or_edit'),
    path('delete/<int:pk>/', views.hunter_delete, name='hunter_delete'),
    path('remove_all/', views.remove_all_hunters, name='remove_all_hunters'),
    path('start_all/', views.start_all_hunters, name='start_all_hunters'),
    path('start/<int:pk>/', views.start_hunter, name='start_hunter'),
    path('stop/<int:pk>/', views.stop_hunter, name='stop_hunter'),
    path('stop_all/', views.stop_all_hunters, name='stop_all_hunters'),
]