"""
Model representing a 'TechnicalAnalysisHunter' which stores settings and configuration
for a user's technical analysis of a specific trading symbol (e.g., BTCUSDC). This model
includes various settings for technical indicators, thresholds, and time periods used in 
market analysis. The model is linked to a specific user and stores the analysis data and 
results for each user.

Attributes:
    user (ForeignKey): The user to whom the technical analysis settings belong.
    symbol (str): The trading symbol (e.g., 'BTCUSDC') for analysis. Default is 'BTCUSDC'.
    interval (str): The time interval for trading data (e.g., '1h'). Default is '1h'.
    lookback (str): The period of historical data to look back for analysis. Default is '1d'.
    comment (str): An optional comment or description for the analysis. Default is an empty string.
    note (str): An optional note field for additional information. Default is an empty string.
    running (bool): A flag indicating if the hunter is running. Default is False.

    trend_signals (bool): A flag to include trend analysis signals. Default is False.
    price_signals (bool): A flag to include price signals. Default is True.
    rsi_signals (bool): A flag to include RSI signals. Default is True.
    rsi_divergence_signals (bool): A flag to include RSI divergence signals. Default is False.
    vol_signals (bool): A flag to include volume signals. Default is True.
    macd_cross_signals (bool): A flag to include MACD cross signals. Default is True.
    macd_histogram_signals (bool): A flag to include MACD histogram signals. Default is False.
    bollinger_signals (bool): A flag to include Bollinger Bands signals. Default is True.
    stoch_signals (bool): A flag to include stochastic oscillator signals. Default is True.
    stoch_divergence_signals (bool): A flag to include stochastic divergence signals. Default is False.
    stoch_rsi_signals (bool): A flag to include stochastic RSI signals. Default is False.
    ema_cross_signals (bool): A flag to include EMA cross signals. Default is False.
    ema_fast_signals (bool): A flag to include fast EMA signals. Default is False.
    ema_slow_signals (bool): A flag to include slow EMA signals. Default is False.
    di_signals (bool): A flag to include Directional Indicator (DI) signals. Default is False.
    cci_signals (bool): A flag to include Commodity Channel Index (CCI) signals. Default is False.
    cci_divergence_signals (bool): A flag to include CCI divergence signals. Default is False.
    mfi_signals (bool): A flag to include Money Flow Index (MFI) signals. Default is False.
    mfi_divergence_signals (bool): A flag to include MFI divergence signals. Default is False.
    atr_signals (bool): A flag to include Average True Range (ATR) signals. Default is False.
    vwap_signals (bool): A flag to include Volume Weighted Average Price (VWAP) signals. Default is False.
    psar_signals (bool): A flag to include Parabolic SAR signals. Default is False.
    ma50_signals (bool): A flag to include 50-period Moving Average signals. Default is False.
    ma200_signals (bool): A flag to include 200-period Moving Average signals. Default is False.
    ma_cross_signals (bool): A flag to include Moving Average crossover signals. Default is False.

    general_timeperiod (int): Time period used for general indicators like RSI, CCI, etc. Default is 14.
    di_timeperiod (int): Time period for Directional Indicator (DI). Default is 14.
    adx_timeperiod (int): Time period for ADX. Default is 14.
    rsi_timeperiod (int): Time period for RSI. Default is 14.
    atr_timeperiod (int): Time period for ATR. Default is 14.
    cci_timeperiod (int): Time period for CCI. Default is 20.
    mfi_timeperiod (int): Time period for MFI. Default is 14.
    macd_timeperiod (int): Time period for MACD. Default is 12.
    macd_signalperiod (int): Signal period for MACD. Default is 9.
    bollinger_timeperiod (int): Time period for Bollinger Bands. Default is 20.
    bollinger_nbdev (int): Number of standard deviations for Bollinger Bands. Default is 2.
    stoch_k_timeperiod (int): Time period for Stochastic %K. Default is 14.
    stoch_d_timeperiod (int): Time period for Stochastic %D. Default is 3.
    stoch_rsi_timeperiod (int): Time period for Stochastic RSI. Default is 14.
    stoch_rsi_k_timeperiod (int): Time period for Stochastic RSI %K. Default is 3.
    stoch_rsi_d_timeperiod (int): Time period for Stochastic RSI %D. Default is 3.
    ema_fast_timeperiod (int): Time period for fast EMA. Default is 9.
    ema_slow_timeperiod (int): Time period for slow EMA. Default is 21.
    psar_acceleration (float): Acceleration factor for Parabolic SAR. Default is 0.02.
    psar_maximum (float): Maximum value for Parabolic SAR. Default is 0.2.

    avg_volume_period (int): Period for calculating average volume. Default is 1.
    avg_close_period (int): Period for calculating average close price. Default is 3.
    avg_adx_period (int): Period for calculating average ADX. Default is 7.
    avg_atr_period (int): Period for calculating average ATR. Default is 28.
    avg_di_period (int): Period for calculating average Directional Indicator. Default is 7.
    avg_rsi_period (int): Period for calculating average RSI. Default is 1.
    avg_stoch_rsi_period (int): Period for calculating average Stochastic RSI. Default is 1.
    avg_macd_period (int): Period for calculating average MACD. Default is 1.
    avg_stoch_period (int): Period for calculating average Stochastic Oscillator. Default is 1.
    avg_ema_period (int): Period for calculating average EMA. Default is 1.
    avg_cci_period (int): Period for calculating average CCI. Default is 1.
    avg_mfi_period (int): Period for calculating average MFI. Default is 1.
    avg_psar_period (int): Period for calculating average PSAR. Default is 1.
    avg_vwap_period (int): Period for calculating average VWAP. Default is 1.

    adx_strong_trend (int): The threshold for a strong ADX trend. Default is 25.
    adx_weak_trend (int): The threshold for a weak ADX trend. Default is 20.
    adx_no_trend (int): The threshold for no ADX trend. Default is 5.

    rsi_buy (int): The RSI value indicating a buy signal. Default is 30.
    rsi_sell (int): The RSI value indicating a sell signal. Default is 70.
    cci_buy (int): The CCI value indicating a buy signal. Default is 30.
    cci_sell (int): The CCI value indicating a sell signal. Default is 70.
    mfi_buy (int): The MFI value indicating a buy signal. Default is 30.
    mfi_sell (int): The MFI value indicating a sell signal. Default is 70.
    stoch_buy (int): The Stochastic value indicating a buy signal. Default is 20.
    stoch_sell (int): The Stochastic value indicating a sell signal. Default is 80.
    atr_buy_threshold (float): The threshold for ATR indicating a buy signal. Default is 0.005.

    df (JSONField): The JSON data containing market data for technical analysis.
    df_last_fetch_time (DateTimeField): The timestamp of the last data fetch.

Methods:
    __str__: Returns a string representation of the model in the format "Ustawienia analizy dla {username}".
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from analysis.models import default_df

class TechnicalAnalysisHunter(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)

    symbol: models.CharField = models.CharField(max_length=10, default='BTCUSDC')
    interval: models.CharField = models.CharField(max_length=10, default='1h')
    lookback: models.CharField = models.CharField(max_length=10, default='1d')
    comment: models.CharField = models.CharField(max_length=1024, default="", blank=True, null=True)
    note: models.CharField = models.CharField(max_length=4096, default="", blank=True, null=True)
    running: models.BooleanField = models.BooleanField(default=False)

    trend_signals: models.BooleanField = models.BooleanField(default=False)
    price_signals: models.BooleanField = models.BooleanField(default=True)
    rsi_signals: models.BooleanField = models.BooleanField(default=True)
    rsi_divergence_signals: models.BooleanField = models.BooleanField(default=False)
    vol_signals: models.BooleanField = models.BooleanField(default=True)
    macd_cross_signals: models.BooleanField = models.BooleanField(default=True)
    macd_histogram_signals: models.BooleanField = models.BooleanField(default=False)
    bollinger_signals: models.BooleanField = models.BooleanField(default=True)
    stoch_signals: models.BooleanField = models.BooleanField(default=True)
    stoch_divergence_signals: models.BooleanField = models.BooleanField(default=False)
    stoch_rsi_signals: models.BooleanField = models.BooleanField(default=False)
    ema_cross_signals: models.BooleanField = models.BooleanField(default=False)
    ema_fast_signals: models.BooleanField = models.BooleanField(default=False)
    ema_slow_signals: models.BooleanField = models.BooleanField(default=False)
    di_signals: models.BooleanField = models.BooleanField(default=False)
    cci_signals: models.BooleanField = models.BooleanField(default=False)
    cci_divergence_signals: models.BooleanField = models.BooleanField(default=False)
    mfi_signals: models.BooleanField = models.BooleanField(default=False)
    mfi_divergence_signals: models.BooleanField = models.BooleanField(default=False)
    atr_signals: models.BooleanField = models.BooleanField(default=False)
    vwap_signals: models.BooleanField = models.BooleanField(default=False)
    psar_signals: models.BooleanField = models.BooleanField(default=False)
    ma50_signals: models.BooleanField = models.BooleanField(default=False)
    ma200_signals: models.BooleanField = models.BooleanField(default=False)
    ma_cross_signals: models.BooleanField = models.BooleanField(default=False)

    general_timeperiod: models.IntegerField = models.IntegerField(default=14)
    di_timeperiod: models.IntegerField = models.IntegerField(default=14)
    adx_timeperiod: models.IntegerField = models.IntegerField(default=14)
    rsi_timeperiod: models.IntegerField = models.IntegerField(default=14)
    atr_timeperiod: models.IntegerField = models.IntegerField(default=14)
    cci_timeperiod: models.IntegerField = models.IntegerField(default=20)
    mfi_timeperiod: models.IntegerField = models.IntegerField(default=14)
    macd_timeperiod: models.IntegerField = models.IntegerField(default=12)
    macd_signalperiod: models.IntegerField = models.IntegerField(default=9)
    bollinger_timeperiod: models.IntegerField = models.IntegerField(default=20)
    bollinger_nbdev: models.IntegerField = models.IntegerField(default=2)
    stoch_k_timeperiod: models.IntegerField = models.IntegerField(default=14)
    stoch_d_timeperiod: models.IntegerField = models.IntegerField(default=3)
    stoch_rsi_timeperiod: models.IntegerField = models.IntegerField(default=14)
    stoch_rsi_k_timeperiod: models.IntegerField = models.IntegerField(default=3)
    stoch_rsi_d_timeperiod: models.IntegerField = models.IntegerField(default=3)
    ema_fast_timeperiod: models.IntegerField = models.IntegerField(default=9)
    ema_slow_timeperiod: models.IntegerField = models.IntegerField(default=21)
    psar_acceleration: models.FloatField = models.FloatField(default=0.02)
    psar_maximum: models.FloatField = models.FloatField(default=0.2)

    avg_volume_period: models.IntegerField = models.IntegerField(default=1)
    avg_close_period: models.IntegerField = models.IntegerField(default=3)
    avg_adx_period: models.IntegerField = models.IntegerField(default=7)
    avg_atr_period: models.IntegerField = models.IntegerField(default=28)
    avg_di_period: models.IntegerField = models.IntegerField(default=7)
    avg_rsi_period: models.IntegerField = models.IntegerField(default=1)
    avg_stoch_rsi_period: models.IntegerField = models.IntegerField(default=1)
    avg_macd_period: models.IntegerField = models.IntegerField(default=1)
    avg_stoch_period: models.IntegerField = models.IntegerField(default=1)
    avg_ema_period: models.IntegerField = models.IntegerField(default=1)
    avg_cci_period: models.IntegerField = models.IntegerField(default=1)
    avg_mfi_period: models.IntegerField = models.IntegerField(default=1)
    avg_psar_period: models.IntegerField = models.IntegerField(default=1)
    avg_vwap_period: models.IntegerField = models.IntegerField(default=1)

    adx_strong_trend: models.IntegerField = models.IntegerField(default=25)
    adx_weak_trend: models.IntegerField = models.IntegerField(default=20)
    adx_no_trend: models.IntegerField = models.IntegerField(default=5)

    rsi_buy: models.IntegerField = models.IntegerField(default=30)
    rsi_sell: models.IntegerField = models.IntegerField(default=70)
    cci_buy: models.IntegerField = models.IntegerField(default=30)
    cci_sell: models.IntegerField = models.IntegerField(default=70)
    mfi_buy: models.IntegerField = models.IntegerField(default=30)
    mfi_sell: models.IntegerField = models.IntegerField(default=70)
    stoch_buy: models.IntegerField = models.IntegerField(default=20)
    stoch_sell: models.IntegerField = models.IntegerField(default=80)
    atr_buy_threshold: models.FloatField = models.FloatField(default=0.005)
    
    df: models.JSONField = models.JSONField(default=default_df)
    df_last_fetch_time: models.DateTimeField = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Hunter settings for {self.user.username}"