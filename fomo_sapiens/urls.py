"""
URL configuration for the FomoSapiensCryptoDipHunter project.

This file contains the URL patterns that map requests to specific views
for the FomoSapiensCryptoDipHunter application. It includes routes for
the home page, account management, CAPTCHA validation, the Django admin
interface, and various app modules such as analysis and hunter.

URL Patterns:
    - '/' (home_page): Renders the home page.
    - '/accounts/': Includes URLs for account management, provided by allauth.
    - '/captcha/': Includes URLs for CAPTCHA validation.
    - '/admin/': URL for the Django admin interface.
    - '/analysis/': Includes URLs for the analysis app.
    - '/hunter/': Includes URLs for the hunter app.

Custom Error Handling:
    - 404 errors are handled by the custom_404_view in fomo_sapiens.views.
"""

from django.contrib import admin
from django.urls import path, include
from fomo_sapiens.views import home_page, custom_404_view

urlpatterns = [
    path("", home_page, name="home_page"),
    path("accounts/", include("allauth.urls")),
    path("captcha/", include("captcha.urls")),
    path("admin/", admin.site.urls),
    path("analysis/", include("analysis.urls")),
    path("hunter/", include("hunter.urls")),
]

handler404 = "fomo_sapiens.views.custom_404_view"
