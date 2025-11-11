"""
Forms for managing user-specific technical analysis settings in the FomoSapiensCryptoDipHunter project.

- `TechnicalAnalysisSettingsForm`: A Django ModelForm that allows users to update their technical analysis settings.
  It includes fields for selecting the trading pair, interval, lookback period, and various technical indicators.
  Widgets are customized with Bootstrap classes for better UI styling.

This form is linked to the `TechnicalAnalysisSettings` model and helps users configure their preferred analysis parameters.
"""

from django import forms
from .models import TechnicalAnalysisSettings


class TechnicalAnalysisSettingsForm(forms.ModelForm):
    class Meta:
        model = TechnicalAnalysisSettings
        fields = [
            "symbol",
            "interval",
            "lookback",
            "general_timeperiod",
            "rsi_timeperiod",
            "rsi_sell",
            "rsi_buy",
            "cci_timeperiod",
            "cci_sell",
            "cci_buy",
            "mfi_timeperiod",
            "mfi_sell",
            "mfi_buy",
            "macd_timeperiod",
            "macd_signalperiod",
            "bollinger_timeperiod",
            "bollinger_nbdev",
            "stoch_k_timeperiod",
            "stoch_d_timeperiod",
            "stoch_rsi_timeperiod",
            "stoch_rsi_k_timeperiod",
            "stoch_rsi_d_timeperiod",
            "ema_fast_timeperiod",
            "ema_slow_timeperiod",
            "psar_acceleration",
            "psar_maximum",
            "atr_timeperiod",
            "di_timeperiod",
            "adx_timeperiod",
            "gpt_model",
            "gpt_prompt"
        ]

        widgets = {
            "symbol": forms.TextInput(attrs={"class": "form-control w-100"}),
            "interval": forms.TextInput(attrs={"class": "form-control w-100"}),
            "lookback": forms.TextInput(attrs={"class": "form-control w-100"}),
            "general_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "rsi_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "cci_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "mfi_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "macd_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "macd_signalperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "bollinger_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "bollinger_nbdev": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "stoch_k_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "stoch_d_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "stoch_rsi_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "stoch_rsi_k_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "stoch_rsi_d_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "ema_fast_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "ema_slow_timeperiod": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "psar_acceleration": forms.NumberInput(
                attrs={"class": "form-control w-100"}
            ),
            "psar_maximum": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "atr_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "di_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "adx_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "rsi_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "rsi_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "cci_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "cci_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "mfi_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "mfi_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
            "gpt_model": forms.TextInput(attrs={"class": "form-control w-100"}),
            "gpt_prompt": forms.TextInput(attrs={"class": "form-control w-100"}),
        }
