"""
URL configuration for FomoSapiensCryptoDipHunter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from fomo_sapiens.views import home_page, custom_404_view
from django_cron import CronJobManager

urlpatterns = [
    path('', home_page, name='home_page'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('analysis/', include('analysis.urls')),
    path('hunter/', include('hunter.urls')),
]

handler404 = "fomo_sapiens.views.custom_404_view"
#cron_manager = CronJobManager()
#cron_manager.run()