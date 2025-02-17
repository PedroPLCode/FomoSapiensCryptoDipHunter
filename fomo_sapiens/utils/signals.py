from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from analysis.models import TechnicalAnalysisSettings
from analysis.utils.fetch_utils import fetch_and_save_df
from django.contrib.auth.models import User
from django.http import HttpRequest
from typing import Dict

@receiver(user_logged_in)
def custom_login_function(sender: type, request: HttpRequest, user: User, **kwargs: Dict) -> None:
    """
    Signal handler for custom logic upon user login.

    This handler is triggered when a user logs in. If the user is authenticated,
    it retrieves or creates their associated TechnicalAnalysisSettings, 
    and fetches and saves the necessary data.

    Args:
        sender (type): The model class that sent the signal.
        request (HttpRequest): The HTTP request object used to process the login.
        user (User): The logged-in user.
        kwargs (dict): Additional arguments passed by the signal.
    """
    if request.user.is_authenticated:
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)
        fetch_and_save_df(user_ta_settings)