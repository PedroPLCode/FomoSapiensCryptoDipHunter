from django import forms
from .models import TechnicalAnalysisHunter

class TechnicalAnalysisHunterForm(forms.ModelForm):
    class Meta:
        model = TechnicalAnalysisHunter
        fields = [
            'symbol', 'interval', 'lookback', 'comment', 'running',
            'trend_signals', 'rsi_signals', 'rsi_divergence_signals', 'vol_signals', 
            'macd_cross_signals', 'macd_histogram_signals', 'bollinger_signals', 
            'stoch_signals', 'stoch_divergence_signals', 'stoch_rsi_signals', 
            'ema_cross_signals', 'ema_fast_signals', 'ema_slow_signals', 'di_signals', 
            'cci_signals', 'cci_divergence_signals', 'mfi_signals', 'mfi_divergence_signals', 
            'atr_signals', 'vwap_signals', 'psar_signals', 'ma50_signals', 'ma200_signals', 
            'ma_cross_signals',
            'general_timeperiod', 'di_timeperiod', 'adx_timeperiod', 'rsi_timeperiod', 
            'atr_timeperiod', 'cci_timeperiod', 'mfi_timeperiod', 'macd_timeperiod', 
            'macd_signalperiod', 'bollinger_timeperiod', 'bollinger_nbdev', 
            'stoch_k_timeperiod', 'stoch_d_timeperiod', 'stoch_rsi_timeperiod', 
            'stoch_rsi_k_timeperiod', 'stoch_rsi_d_timeperiod', 'ema_fast_timeperiod', 
            'ema_slow_timeperiod', 'psar_acceleration', 'psar_maximum', 'avg_volume_period', 
            'avg_close_period', 'avg_adx_period', 'avg_atr_period', 'avg_di_period', 
            'avg_rsi_period', 'avg_stoch_rsi_period', 'avg_macd_period', 'avg_stoch_period', 
            'avg_ema_period', 'avg_cci_period', 'avg_mfi_period', 'avg_psar_period', 
            'avg_vwap_period', 'adx_strong_trend', 'adx_weak_trend', 'adx_no_trend', 
            'rsi_buy', 'rsi_sell', 'cci_buy', 'cci_sell', 'mfi_buy', 'mfi_sell', 'stoch_buy', 
            'stoch_sell', 'atr_buy_threshold'
        ]