from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from analysis.models import TechnicalAnalysisSettings
from analysis.utils.fetch_utils import fetch_and_save_df
from django.contrib.auth.models import User
from django.http import HttpRequest
from typing import Dict


@receiver(post_save, sender=User)
def create_user_profile(
    sender: type, instance: User, created: bool, **kwargs: Dict
) -> None:
    """
    This function is triggered after a new User instance is saved.
    It sends an email notification to the admin and logs the new user's information.

    Args:
        sender: The model class that sent the signal (User).
        instance: The instance of the User model that was saved.
        created: A boolean indicating whether a new instance was created (True) or updated (False).
        **kwargs: Additional keyword arguments that may be passed.
    """
    if created:
        from datetime import datetime
        from fomo_sapiens.utils.email_utils import send_admin_email
        from fomo_sapiens.utils.logging import logger

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"New user created: {instance.username}")

        send_admin_email(
            "New user created",
            f"New user has been created and added to db\n"
            f"{formatted_now}\n\n"
            f"User {instance.username} {instance.email} {instance.is_superuser} {instance.date_joined}",
        )


@receiver(user_logged_in)
def custom_login_function(
    sender: type, request: HttpRequest, user: User, **kwargs: Dict
) -> None:
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
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
            user=request.user
        )
        fetch_and_save_df(user_ta_settings)
