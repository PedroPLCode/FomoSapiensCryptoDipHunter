from DipHunterCryptoTechnicalAnalysis.utils.logging import logger
from DipHunterCryptoTechnicalAnalysis.utils.exception_handlers import exception_handler

@exception_handler(default_return=False)
def trend_buy_signal(trend, hunter_settings):
    """
    Determines whether to trigger a buy signal based on the current trend.

    Args:
        trend (str): The current trend ('uptrend' or 'downtrend').
        hunter_settings (object): The bot settings containing trend signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.trend_signals:
        return (trend == 'uptrend')
    return True


@exception_handler(default_return=False)
def rsi_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on the RSI values.

    Args:
        latest_data (dict): The latest market data including RSI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing RSI buy preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.rsi_signals:
        return (float(latest_data['rsi']) <= float(hunter_settings.rsi_buy) and
                float(latest_data['rsi']) >= float(averages['avg_rsi'])) 
    return True


@exception_handler(default_return=False)
def rsi_divergence_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on RSI divergence.

    Args:
        latest_data (dict): The latest market data including RSI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing RSI divergence signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.rsi_divergence_signals:
        return (float(latest_data['close']) <= float(averages['avg_close']) and
                float(latest_data['rsi']) >= float(averages['avg_rsi'])) 
    return True


@exception_handler(default_return=False)
def vol_rising(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on increasing volume.

    Args:
        latest_data (dict): The latest market data including volume.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing volume signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.vol_signals:
        return float(latest_data['volume']) >= float(averages['avg_volume']) 
    return True


@exception_handler(default_return=False)
def macd_cross_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on MACD cross.

    Args:
        latest_data (dict): The latest market data including MACD values.
        previous_data (dict): The previous market data including MACD values.
        hunter_settings (object): The bot settings containing MACD cross signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.macd_cross_signals:
        return (float(previous_data['macd']) <= float(previous_data['macd_signal']) and
                float(latest_data['macd']) >= float(latest_data['macd_signal'])) 
    return True


@exception_handler(default_return=False)
def macd_histogram_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on MACD histogram.

    Args:
        latest_data (dict): The latest market data including MACD histogram.
        previous_data (dict): The previous market data including MACD histogram.
        hunter_settings (object): The bot settings containing MACD histogram signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.macd_histogram_signals:
        return (float(previous_data['macd_histogram']) <= 0 and
                float(latest_data['macd_histogram']) >= 0) 
    return True


@exception_handler(default_return=False)
def bollinger_buy_signal(latest_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Bollinger Bands.

    Args:
        latest_data (dict): The latest market data including close price and lower band.
        hunter_settings (object): The bot settings containing Bollinger Band signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.bollinger_signals:
        return float(latest_data['close']) <= float(latest_data['lower_band'])
    return True


@exception_handler(default_return=False)
def stoch_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Stochastic Oscillator.

    Args:
        latest_data (dict): The latest market data including stochastic values.
        previous_data (dict): The previous market data including stochastic values.
        hunter_settings (object): The bot settings containing stochastic signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.stoch_signals:
        return (float(previous_data['stoch_k']) <= float(previous_data['stoch_d']) and
                float(latest_data['stoch_k']) >= float(latest_data['stoch_d']) and
                float(latest_data['stoch_k']) <= float(hunter_settings.stoch_buy)) 
    return True


@exception_handler(default_return=False)
def stoch_divergence_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Stochastic Divergence.

    Args:
        latest_data (dict): The latest market data including stochastic values.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing stochastic divergence signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.stoch_divergence_signals:
        return (float(latest_data['stoch_k']) >= float(averages['avg_stoch_k']) and
                float(latest_data['close']) <= float(averages['avg_close'])) 
    return True


@exception_handler(default_return=False)
def stoch_rsi_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Stochastic RSI.

    Args:
        latest_data (dict): The latest market data including Stochastic RSI values.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing Stochastic RSI signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.stoch_rsi_signals:
        return (float(latest_data['stoch_rsi_k']) <= float(hunter_settings.stoch_buy) and
                float(latest_data['stoch_rsi_k']) >= float(averages['avg_stoch_rsi_k'])) 
    return True


@exception_handler(default_return=False)
def ema_cross_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on EMA cross.

    Args:
        latest_data (dict): The latest market data including EMA values.
        previous_data (dict): The previous market data including EMA values.
        hunter_settings (object): The bot settings containing EMA cross signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ema_cross_signals:
        return (float(previous_data['ema_fast']) <= float(previous_data['ema_slow']) and
                float(latest_data['ema_fast']) >= float(latest_data['ema_slow'])) 
    return True


@exception_handler(default_return=False)
def ema_fast_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on fast EMA.

    Args:
        latest_data (dict): The latest market data including close price and fast EMA.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing fast EMA signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ema_fast_signals:
        return float(latest_data['close']) >= float(averages['avg_ema_fast']) 
    return True


@exception_handler(default_return=False)
def ema_slow_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on slow EMA.

    Args:
        latest_data (dict): The latest market data including close price and slow EMA.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing slow EMA signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ema_slow_signals:
        return float(latest_data['close']) >= float(averages['avg_ema_slow']) 
    return True


@exception_handler(default_return=False)
def di_cross_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Directional Indicator cross.

    Args:
        latest_data (dict): The latest market data including Directional Indicator values.
        previous_data (dict): The previous market data including Directional Indicator values.
        hunter_settings (object): The bot settings containing DI signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.di_signals:
        return (float(previous_data['plus_di']) <= float(previous_data['minus_di']) and
                    float(latest_data['plus_di']) >= float(latest_data['minus_di'])) 
    return True
    

@exception_handler(default_return=False)
def cci_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Commodity Channel Index (CCI).

    Args:
        latest_data (dict): The latest market data including CCI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing CCI signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.cci_signals:
        return (float(latest_data['cci']) <= float(hunter_settings.cci_buy) and
                float(latest_data['cci']) >= float(averages['avg_cci']))  
    return True


@exception_handler(default_return=False)
def cci_divergence_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on CCI divergence.

    Args:
        latest_data (dict): The latest market data including CCI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing CCI divergence signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.cci_divergence_signals:
        return (float(latest_data['close']) <= float(averages['avg_close']) and
                float(latest_data['cci']) >= float(averages['avg_cci'])) 
    return True


@exception_handler(default_return=False)
def mfi_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Money Flow Index (MFI).

    Args:
        latest_data (dict): The latest market data including MFI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing MFI signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.mfi_signals:
        return (float(latest_data['mfi']) <= float(hunter_settings.mfi_buy) and
                float(latest_data['mfi']) >= float(averages['avg_mfi'])) 
    return True


@exception_handler(default_return=False)
def mfi_divergence_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on MFI divergence.

    Args:
        latest_data (dict): The latest market data including MFI.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing MFI divergence signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.mfi_divergence_signals:
        return (float(latest_data['close']) <= float(averages['avg_close']) and
                float(latest_data['mfi']) >= float(averages['avg_mfi'])) 
    return True


@exception_handler(default_return=False)
def atr_buy_signal(latest_data, averages, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Average True Range (ATR).

    Args:
        latest_data (dict): The latest market data including ATR.
        averages (dict): The average market data for comparison.
        hunter_settings (object): The bot settings containing ATR signal preference.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.atr_signals:
        atr_buy_level = hunter_settings.atr_buy_treshold * float(latest_data['close'])
        return (float(latest_data['atr']) >= float(averages['avg_atr']) and
                float(latest_data['atr']) >= float(atr_buy_level))
    return True


@exception_handler(default_return=False)
def vwap_buy_signal(latest_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on VWAP.

    Args:
        latest_data (dict): The latest market data including VWAP.
        hunter_settings (object): The bot settings signals preferences.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.vwap_signals:
        return float(latest_data['close']) >= float(latest_data['vwap']) 
    return True
    

@exception_handler(default_return=False)
def psar_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Parabolic SAR (PSAR).

    Args:
        latest_data (dict): The latest market data including PSAR.
        previous_data (dict): The previous market data including PSAR.
        hunter_settings (object): The bot settings containing signals preferences.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.psar_signals:
        return (float(previous_data['psar']) >= float(previous_data['close']) and
                float(latest_data['psar']) <= float(latest_data['close'])) 
    return True


@exception_handler(default_return=False)
def ma50_buy_signal(latest_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Moving Average (MA50).

    Args:
        latest_data (dict): The latest market data including MA50.
        hunter_settings (object): The bot settings containing signals preferences.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ma50_signals:
        return float(latest_data['close']) >= float(latest_data['ma_50']) 
    return True


@exception_handler(default_return=False)
def ma200_buy_signal(latest_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Moving Average (MA200).

    Args:
        latest_data (dict): The latest market data including MA200.
        hunter_settings (object): The bot settings containing signals preferences.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ma200_signals:
        return float(latest_data['close']) >= float(latest_data['ma_200']) 
    return True


@exception_handler(default_return=False)
def ma_cross_buy_signal(latest_data, previous_data, hunter_settings):
    """
    Determines whether to trigger a buy signal based on Moving Averages (MA50 and MA200).

    Args:
        latest_data (dict): The latest market data including MA50 and MA200.
        hunter_settings (object): The bot settings containing signals preferences.

    Returns:
        bool: True if the buy signal should be triggered, otherwise False.
    """
    if hunter_settings.ma_cross_signals:
        return (float(previous_data['ma_50']) <= float(previous_data['ma_200']) and
                    float(latest_data['ma_50']) >= float(latest_data['ma_200'])) 
    return True
    

@exception_handler(default_return=False)
def check_classic_ta_buy_signal(
    df, 
    hunter_settings, 
    trend, 
    averages, 
    ):
    """
    Calculates whether a buy signal should be triggered based on multiple conditions.

    Args:
        latest_data (dict): The latest market data.
        previous_data (dict): The previous market data.
        averages (dict): The average market data.
        hunter_settings (object): The bot settings containing the various signal preferences.

    Returns:
        bool: True if a buy signal is triggered, otherwise False.
    """
    from .logic_utils import is_df_valid
    
    if not is_df_valid(df, hunter_settings.id):
        return False
    
    latest_data = df.iloc[-1]
    previous_data = df.iloc[-2]
    
    if trend == 'downtrend':
        return False

    buy_signals = [
        trend_buy_signal(trend, hunter_settings),
        rsi_buy_signal(latest_data, averages, hunter_settings),
        rsi_divergence_buy_signal(latest_data, averages, hunter_settings),
        vol_rising(latest_data, averages, hunter_settings),
        macd_cross_buy_signal(latest_data, previous_data, hunter_settings),
        macd_histogram_buy_signal(latest_data, previous_data, hunter_settings),
        bollinger_buy_signal(latest_data, hunter_settings),
        stoch_buy_signal(latest_data, previous_data, hunter_settings),
        stoch_divergence_buy_signal(latest_data, averages, hunter_settings),
        stoch_rsi_buy_signal(latest_data, averages, hunter_settings),
        ema_cross_buy_signal(latest_data, previous_data, hunter_settings),
        ema_fast_buy_signal(latest_data, averages, hunter_settings),
        ema_slow_buy_signal(latest_data, averages, hunter_settings),
        di_cross_buy_signal(latest_data, previous_data, hunter_settings),
        cci_buy_signal(latest_data, averages, hunter_settings),
        cci_divergence_buy_signal(latest_data, averages, hunter_settings),
        mfi_buy_signal(latest_data, averages, hunter_settings),
        mfi_divergence_buy_signal(latest_data, averages, hunter_settings),
        atr_buy_signal(latest_data, averages, hunter_settings),
        vwap_buy_signal(latest_data, hunter_settings),
        psar_buy_signal(latest_data, previous_data, hunter_settings),
        ma50_buy_signal(latest_data, hunter_settings),
        ma200_buy_signal(latest_data, hunter_settings),
        ma_cross_buy_signal(latest_data, previous_data, hunter_settings)
    ]
    
    signals_to_check = [bool(signal) for signal in buy_signals]

    if all(signals_to_check):
        return True
    
    return False