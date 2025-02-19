from django import forms
from .models import TechnicalAnalysisHunter


class TechnicalAnalysisHunterForm(forms.ModelForm):
    """
    A Django form for the TechnicalAnalysisHunter model, which allows
    the user to input and update settings for technical analysis indicators
    and strategies used in financial trading.

    Fields include various technical analysis indicators like RSI, MACD,
    Bollinger Bands, EMA, and others, with options to configure parameters
    for trend signals, buy/sell conditions, time periods, and more.

    Attributes:
        symbol (str): The trading symbol (e.g., "BTCUSD").
        interval (str): The trading interval (e.g., "1m", "5m").
        lookback (int): The number of periods to look back for analysis.
        comment (str): A comment or description for the setup.
        running (bool): A flag to indicate whether the strategy is running.
        general_timeperiod (int): A general time period used across various indicators.
        price_signals (bool): Whether to use price-based signals.
        avg_close_period (int): The period for calculating the average closing price.
        trend_signals (bool): Whether to use trend-based signals.
        adx_timeperiod (int): The period for the ADX indicator.
        adx_strong_trend (int): Threshold for strong trend in ADX.
        adx_weak_trend (int): Threshold for weak trend in ADX.
        adx_no_trend (int): Threshold for no trend in ADX.
        avg_adx_period (int): The period for calculating the average ADX.
        rsi_signals (bool): Whether to use RSI signals.
        rsi_divergence_signals (bool): Whether to use RSI divergence signals.
        rsi_timeperiod (int): The time period for the RSI indicator.
        rsi_buy (int): The RSI level to trigger a buy signal.
        rsi_sell (int): The RSI level to trigger a sell signal.
        avg_rsi_period (int): The period for calculating the average RSI.
        vol_signals (bool): Whether to use volume-based signals.
        avg_volume_period (int): The period for calculating the average volume.
        macd_cross_signals (bool): Whether to use MACD crossover signals.
        macd_histogram_signals (bool): Whether to use MACD histogram signals.
        macd_timeperiod (int): The time period for the MACD.
        macd_signalperiod (int): The signal period for the MACD.
        avg_macd_period (int): The period for calculating the average MACD.
        bollinger_signals (bool): Whether to use Bollinger Bands signals.
        bollinger_timeperiod (int): The time period for the Bollinger Bands.
        bollinger_nbdev (float): The number of standard deviations for the Bollinger Bands.
        stoch_signals (bool): Whether to use stochastic signals.
        stoch_divergence_signals (bool): Whether to use stochastic divergence signals.
        stoch_k_timeperiod (int): The time period for the stochastic %K line.
        stoch_d_timeperiod (int): The time period for the stochastic %D line.
        stoch_buy (int): The stochastic level to trigger a buy signal.
        stoch_sell (int): The stochastic level to trigger a sell signal.
        avg_stoch_period (int): The period for calculating the average stochastic.
        stoch_rsi_signals (bool): Whether to use stochastic RSI signals.
        stoch_rsi_timeperiod (int): The time period for the stochastic RSI.
        stoch_rsi_k_timeperiod (int): The time period for the stochastic RSI %K line.
        stoch_rsi_d_timeperiod (int): The time period for the stochastic RSI %D line.
        avg_stoch_rsi_period (int): The period for calculating the average stochastic RSI.
        ema_cross_signals (bool): Whether to use EMA crossover signals.
        ema_fast_signals (bool): Whether to use fast EMA signals.
        ema_slow_signals (bool): Whether to use slow EMA signals.
        ema_fast_timeperiod (int): The time period for the fast EMA.
        ema_slow_timeperiod (int): The time period for the slow EMA.
        avg_ema_period (int): The period for calculating the average EMA.
        di_signals (bool): Whether to use the Directional Indicator signals.
        di_timeperiod (int): The time period for the Directional Indicator.
        avg_di_period (int): The period for calculating the average DI.
        cci_signals (bool): Whether to use the Commodity Channel Index signals.
        cci_divergence_signals (bool): Whether to use CCI divergence signals.
        cci_timeperiod (int): The time period for the CCI.
        cci_buy (int): The CCI level to trigger a buy signal.
        cci_sell (int): The CCI level to trigger a sell signal.
        avg_cci_period (int): The period for calculating the average CCI.
        mfi_signals (bool): Whether to use the Money Flow Index signals.
        mfi_divergence_signals (bool): Whether to use MFI divergence signals.
        mfi_timeperiod (int): The time period for the MFI.
        mfi_buy (int): The MFI level to trigger a buy signal.
        mfi_sell (int): The MFI level to trigger a sell signal.
        avg_mfi_period (int): The period for calculating the average MFI.
        atr_signals (bool): Whether to use the Average True Range signals.
        atr_timeperiod (int): The time period for the ATR.
        atr_buy_threshold (float): The threshold for buying based on ATR.
        avg_atr_period (int): The period for calculating the average ATR.
        vwap_signals (bool): Whether to use VWAP signals.
        avg_vwap_period (int): The period for calculating the average VWAP.
        psar_signals (bool): Whether to use the Parabolic SAR signals.
        psar_acceleration (float): The acceleration factor for the PSAR.
        psar_maximum (float): The maximum value for the PSAR.
        avg_psar_period (int): The period for calculating the average PSAR.
        ma50_signals (bool): Whether to use the 50-period moving average signals.
        ma200_signals (bool): Whether to use the 200-period moving average signals.
        ma_cross_signals (bool): Whether to use moving average crossover signals.
        note (str): A note or additional comment for the configuration.

    The form uses Django's ModelForm to create and manage instances of
    the TechnicalAnalysisHunter model.
    """

    class Meta:
        model = TechnicalAnalysisHunter
        fields = [
            "symbol",
            "interval",
            "lookback",
            "comment",
            "running",
            "general_timeperiod",
            "price_signals",
            "avg_close_period",
            "trend_signals",
            "adx_timeperiod",
            "adx_strong_trend",
            "adx_weak_trend",
            "adx_no_trend",
            "avg_adx_period",
            "rsi_signals",
            "rsi_divergence_signals",
            "rsi_timeperiod",
            "rsi_buy",
            "rsi_sell",
            "avg_rsi_period",
            "vol_signals",
            "avg_volume_period",
            "macd_cross_signals",
            "macd_histogram_signals",
            "macd_timeperiod",
            "macd_signalperiod",
            "avg_macd_period",
            "bollinger_signals",
            "bollinger_timeperiod",
            "bollinger_nbdev",
            "stoch_signals",
            "stoch_divergence_signals",
            "stoch_k_timeperiod",
            "stoch_d_timeperiod",
            "stoch_buy",
            "stoch_sell",
            "avg_stoch_period",
            "stoch_rsi_signals",
            "stoch_rsi_timeperiod",
            "stoch_rsi_k_timeperiod",
            "stoch_rsi_d_timeperiod",
            "avg_stoch_rsi_period",
            "ema_cross_signals",
            "ema_fast_signals",
            "ema_slow_signals",
            "ema_fast_timeperiod",
            "ema_slow_timeperiod",
            "avg_ema_period",
            "di_signals",
            "di_timeperiod",
            "avg_di_period",
            "cci_signals",
            "cci_divergence_signals",
            "cci_timeperiod",
            "cci_buy",
            "cci_sell",
            "avg_cci_period",
            "mfi_signals",
            "mfi_divergence_signals",
            "mfi_timeperiod",
            "mfi_buy",
            "mfi_sell",
            "avg_mfi_period",
            "atr_signals",
            "atr_timeperiod",
            "atr_buy_threshold",
            "avg_atr_period",
            "vwap_signals",
            "avg_vwap_period",
            "psar_signals",
            "psar_acceleration",
            "psar_maximum",
            "avg_psar_period",
            "ma50_signals",
            "ma200_signals",
            "ma_cross_signals",
            "note",
        ]

    widgets = {
        "symbol": forms.TextInput(attrs={"class": "form-control w-100"}),
        "interval": forms.TextInput(attrs={"class": "form-control w-100"}),
        "lookback": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "comment": forms.Textarea(attrs={"class": "form-control w-100", "rows": 3}),
        "running": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "general_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "price_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "avg_close_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "trend_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "adx_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "adx_strong_trend": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "adx_weak_trend": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "adx_no_trend": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_adx_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "rsi_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "rsi_divergence_signals": forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        "rsi_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "rsi_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "rsi_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_rsi_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "vol_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "avg_volume_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "macd_cross_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "macd_histogram_signals": forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        "macd_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "macd_signalperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_macd_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "bollinger_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "bollinger_timeperiod": forms.NumberInput(
            attrs={"class": "form-control w-100"}
        ),
        "bollinger_nbdev": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "stoch_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "stoch_divergence_signals": forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        "stoch_k_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "stoch_d_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "stoch_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "stoch_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_stoch_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "stoch_rsi_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "stoch_rsi_timeperiod": forms.NumberInput(
            attrs={"class": "form-control w-100"}
        ),
        "stoch_rsi_k_timeperiod": forms.NumberInput(
            attrs={"class": "form-control w-100"}
        ),
        "stoch_rsi_d_timeperiod": forms.NumberInput(
            attrs={"class": "form-control w-100"}
        ),
        "avg_stoch_rsi_period": forms.NumberInput(
            attrs={"class": "form-control w-100"}
        ),
        "ema_cross_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "ema_fast_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "ema_slow_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "ema_fast_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "ema_slow_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_ema_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "di_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "di_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_di_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "cci_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "cci_divergence_signals": forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        "cci_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "cci_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "cci_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_cci_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "mfi_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "mfi_divergence_signals": forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        "mfi_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "mfi_buy": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "mfi_sell": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_mfi_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "atr_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "atr_timeperiod": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "atr_buy_threshold": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_atr_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "vwap_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "avg_vwap_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "psar_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "psar_acceleration": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "psar_maximum": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "avg_psar_period": forms.NumberInput(attrs={"class": "form-control w-100"}),
        "ma50_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "ma200_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "ma_cross_signals": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "note": forms.Textarea(attrs={"class": "form-control w-100", "rows": 3}),
    }
