"""
Models and signals for managing technical analysis settings in the FomoSapiensCryptoDipHunter project.

- `TechnicalAnalysisSettings`: Stores user-specific settings for technical analysis, including indicators, time periods, and fetched data.
- `create_user_analysis_settings`: Signal that creates default technical analysis settings when a new user is created.
- `save_user_analysis_settings`: Signal that saves the user's analysis settings whenever the user object is saved.
- `default_plot_indicators`: Returns a default list of selected indicators for plotting.
- `default_df`: Fetches and returns default market data in JSON format.

This module integrates with Django's `User` model and uses signals to automate settings creation.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=User)
def create_user_analysis_settings(sender, instance, created, **kwargs):
    if created:
        if instance.is_authenticated:
            TechnicalAnalysisSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_analysis_settings(sender, instance, **kwargs):
    instance.technicalanalysissettings.save()
    
def default_plot_indicators():
    return ['rsi', 'macd']

def default_df():
    from .utils.fetch_utils import fetch_data
    df_fetched = fetch_data('BTCUSDC')
    json_df = df_fetched.to_json(orient='records')
    return json_df

class TechnicalAnalysisSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    symbol = models.CharField(max_length=10, default='BTCUSDC')
    interval = models.CharField(max_length=10, default='1h')
    lookback = models.CharField(max_length=10, default='1d')
    
    general_timeperiod = models.IntegerField(default=14)
    di_timeperiod = models.IntegerField(default=14)
    adx_timeperiod = models.IntegerField(default=14)
    rsi_timeperiod = models.IntegerField(default=14)
    atr_timeperiod = models.IntegerField(default=14)
    cci_timeperiod = models.IntegerField(default=20)
    mfi_timeperiod = models.IntegerField(default=14)
    macd_timeperiod = models.IntegerField(default=12)
    macd_signalperiod = models.IntegerField(default=9)
    bollinger_timeperiod = models.IntegerField(default=20)
    bollinger_nbdev = models.IntegerField(default=2)
    stoch_k_timeperiod = models.IntegerField(default=14)
    stoch_d_timeperiod = models.IntegerField(default=3)
    stoch_rsi_timeperiod = models.IntegerField(default=14)
    stoch_rsi_k_timeperiod = models.IntegerField(default=3)
    stoch_rsi_d_timeperiod = models.IntegerField(default=3)
    ema_fast_timeperiod = models.IntegerField(default=9)
    ema_slow_timeperiod = models.IntegerField(default=21)
    psar_acceleration = models.FloatField(default=0.02)
    psar_maximum = models.FloatField(default=0.2)
    
    adx_strong_trend = models.IntegerField(default=25)
    adx_weak_trend = models.IntegerField(default=20)
    adx_no_trend = models.IntegerField(default=5)
    
    rsi_buy = models.IntegerField(default=30)
    rsi_sell = models.IntegerField(default=70)
    cci_buy = models.IntegerField(default=30)
    cci_sell = models.IntegerField(default=70)
    mfi_buy = models.IntegerField(default=30)
    mfi_sell = models.IntegerField(default=70)
    stoch_buy = models.IntegerField(default=30)
    stoch_sell = models.IntegerField(default=70)
    atr_buy_threshold = models.FloatField(default=0.005)
    
    selected_plot_indicators = models.JSONField(default=default_plot_indicators)
    
    df = models.JSONField(default=default_df)
    df_last_fetch_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Technical Analysis settings for {self.user.username}"