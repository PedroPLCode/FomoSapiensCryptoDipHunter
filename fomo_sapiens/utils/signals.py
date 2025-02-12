from django.contrib.auth.signals import user_logged_in#, user_signed_up
from django.dispatch import receiver
from analysis.models import TechnicalAnalysisSettings
from analysis.utils.fetch_utils import fetch_and_save_df
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import IntegrityError

@receiver(user_logged_in)
def make_first_user_superuser(sender, request, user, **kwargs):
    if User.objects.count() == 1:
        user.is_superuser = True
        user.is_staff = True
        user.save()


@receiver(user_logged_in)
def custom_login_function(sender, request, user, **kwargs):
    if request.user.is_authenticated:
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)
        fetch_and_save_df(user_ta_settings)