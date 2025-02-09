from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from analysis.models import TechnicalAnalysisSettings
from analysis.utils.fetch_utils import fetch_and_save_df

@receiver(user_logged_in)
def custom_login_function(sender, request, user, **kwargs):
    if request.user.is_authenticated:
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)
        fetch_and_save_df(user_ta_settings)