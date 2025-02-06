from django.urls import path
from . import views

app_name = 'hunter'

urlpatterns = [
    path('', views.hunter_list, name='hunter_list'),
    path('create/', views.hunter_create, name='hunter_create'),
    path('edit/<int:pk>/', views.hunter_edit, name='hunter_edit'),
    path('delete/<int:pk>/', views.hunter_delete, name='hunter_delete'),
]