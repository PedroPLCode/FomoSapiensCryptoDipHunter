from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_analysis_settings(sender, instance, created, **kwargs):
    if created:
        if instance.is_authenticated:
            TechnicalAnalysisHunter.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_analysis_settings(sender, instance, **kwargs):
    try:
        instance.technicalanalysishunter.save()
    except TechnicalAnalysisHunter.DoesNotExist:
        pass

class TechnicalAnalysisHunter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    symbol = models.CharField(max_length=10, default='BTCUSDC')
    interval = models.CharField(max_length=10, default='1h')
    lookback = models.CharField(max_length=10, default='9d')
    comment = models.CharField(max_length=1024, default="comment", blank=True, null=True)
    running = models.BooleanField(default=False)

    trend_signals = models.BooleanField(default=False)
    rsi_signals = models.BooleanField(default=True)
    rsi_divergence_signals = models.BooleanField(default=False)
    vol_signals = models.BooleanField(default=True)
    macd_cross_signals = models.BooleanField(default=True)
    macd_histogram_signals = models.BooleanField(default=False)
    bollinger_signals = models.BooleanField(default=True)
    stoch_signals = models.BooleanField(default=True)
    stoch_divergence_signals = models.BooleanField(default=False)
    stoch_rsi_signals = models.BooleanField(default=False)
    ema_cross_signals = models.BooleanField(default=False)
    ema_fast_signals = models.BooleanField(default=False)
    ema_slow_signals = models.BooleanField(default=False)
    di_signals = models.BooleanField(default=False)
    cci_signals = models.BooleanField(default=False)
    cci_divergence_signals = models.BooleanField(default=False)
    mfi_signals = models.BooleanField(default=False)
    mfi_divergence_signals = models.BooleanField(default=False)
    atr_signals = models.BooleanField(default=False)
    vwap_signals = models.BooleanField(default=False)
    psar_signals = models.BooleanField(default=False)
    ma50_signals = models.BooleanField(default=False)
    ma200_signals = models.BooleanField(default=False)
    ma_cross_signals = models.BooleanField(default=False)

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

    avg_volume_period = models.IntegerField(default=1)
    avg_close_period = models.IntegerField(default=3)
    avg_adx_period = models.IntegerField(default=7)
    avg_atr_period = models.IntegerField(default=28)
    avg_di_period = models.IntegerField(default=7)
    avg_rsi_period = models.IntegerField(default=1)
    avg_stoch_rsi_period = models.IntegerField(default=1)
    avg_macd_period = models.IntegerField(default=1)
    avg_stoch_period = models.IntegerField(default=1)
    avg_ema_period = models.IntegerField(default=1)
    avg_cci_period = models.IntegerField(default=1)
    avg_mfi_period = models.IntegerField(default=1)
    avg_psar_period = models.IntegerField(default=1)
    avg_vwap_period = models.IntegerField(default=1)

    adx_strong_trend = models.IntegerField(default=25)
    adx_weak_trend = models.IntegerField(default=20)
    adx_no_trend = models.IntegerField(default=5)

    rsi_buy = models.IntegerField(default=30)
    rsi_sell = models.IntegerField(default=70)
    cci_buy = models.IntegerField(default=30)
    cci_sell = models.IntegerField(default=70)
    mfi_buy = models.IntegerField(default=30)
    mfi_sell = models.IntegerField(default=70)
    stoch_buy = models.IntegerField(default=20)
    stoch_sell = models.IntegerField(default=80)
    atr_buy_threshold = models.FloatField(default=0.005)

    def __str__(self):
        return f"Ustawienia analizy dla {self.user.username}"