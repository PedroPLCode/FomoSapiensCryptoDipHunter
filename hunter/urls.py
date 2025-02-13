from django.urls import path
from . import views

app_name = 'hunter'

urlpatterns = [
    path('', views.hunter_list, name='hunter_list'),
    path('create_edit/<int:pk>/', views.hunter_create_or_edit, name='hunter_create_or_edit'),
    path('delete/<int:pk>/', views.hunter_delete, name='hunter_delete'),
    path('start_all/', views.start_all_hunters, name='start_all_hunters'),
    path('start/<int:pk>/', views.start_hunter, name='start_hunter'),
    path('stop/<int:pk>/', views.stop_hunter, name='stop_hunter'),
    path('stop_all/', views.stop_all_hunters, name='stop_all_hunters'),
]