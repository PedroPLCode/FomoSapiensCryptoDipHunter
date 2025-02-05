from django import forms
from .models import UserTechnicalAnalysisSettings

class UserTechnicalAnalysisSettingsForm(forms.ModelForm):
    class Meta:
        model = UserTechnicalAnalysisSettings
        fields = ['symbol',
                  'interval',
                  'general_timeperiod',
                  'rsi_timeperiod',
                  'cci_timeperiod',
                  'mfi_timeperiod',
                  'macd_timeperiod',
                  'macd_signalperiod',
                  'bollinger_timeperiod',
                  'bollinger_nbdev',
                  'stoch_k_timeperiod',
                  'stoch_d_timeperiod',
                  'stoch_rsi_timeperiod',
                  'stoch_rsi_k_timeperiod',
                  'stoch_rsi_d_timeperiod',
                  'ema_fast_timeperiod',
                  'ema_slow_timeperiod',
                  'psar_acceleration',
                  'psar_maximum',
                  'atr_timeperiod',
                  'di_timeperiod',
                  'adx_timeperiod',
                  'rsi_sell',
                  'rsi_buy',
                  'cci_sell',
                  'cci_buy',
                  'mfi_sell',
                  'mfi_buy',
                  ]