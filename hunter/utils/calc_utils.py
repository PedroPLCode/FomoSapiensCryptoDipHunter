from DipHunterCryptoTechnicalAnalysis.utils.logging import logger
from DipHunterCryptoTechnicalAnalysis.utils.exception_handlers import exception_handler

@exception_handler()
def calculate_ta_averages(df, hunter_settings):
    """
    Calculates the average values for various technical analysis indicators.

    This function computes the average of specific columns in the DataFrame over a defined period,
    based on the bot settings. The calculated averages are returned as a dictionary.

    Args:
        df (pandas.DataFrame): The DataFrame containing the market data.
        hunter_settings (object): The settings for the bot, including the periods for averaging the indicators.

    Returns:
        dict: A dictionary containing the average values of technical indicators, or None if an error occurs.
    """
    averages = {}
    
    average_mappings = {
        'avg_volume': ('volume', hunter_settings.avg_volume_period),
        'avg_rsi': ('rsi', hunter_settings.avg_rsi_period),
        'avg_cci': ('cci', hunter_settings.avg_cci_period),
        'avg_mfi': ('mfi', hunter_settings.avg_mfi_period),
        'avg_atr': ('atr', hunter_settings.avg_atr_period),
        'avg_stoch_rsi_k': ('stoch_rsi_k', hunter_settings.avg_stoch_rsi_period),
        'avg_macd': ('macd', hunter_settings.avg_macd_period),
        'avg_macd_signal': ('macd_signal', hunter_settings.avg_macd_period),
        'avg_stoch_k': ('stoch_k', hunter_settings.avg_stoch_period),
        'avg_stoch_d': ('stoch_d', hunter_settings.avg_stoch_period),
        'avg_ema_fast': ('ema_fast', hunter_settings.avg_ema_period),
        'avg_ema_slow': ('ema_slow', hunter_settings.avg_ema_period),
        'avg_plus_di': ('plus_di', hunter_settings.avg_di_period),
        'avg_minus_di': ('minus_di', hunter_settings.avg_di_period),
        'avg_psar': ('psar', hunter_settings.avg_psar_period),
        'avg_vwap': ('vwap', hunter_settings.avg_vwap_period),
        'avg_close': ('close', hunter_settings.avg_close_period),
    }

    for avg_name, (column, period) in average_mappings.items():
        averages[avg_name] = df[column].iloc[-period:].mean()

    return averages


@exception_handler(default_return='none')
def check_ta_trend(df, hunter_settings):
    """
    Checks the market trend based on technical analysis indicators.

    This function evaluates the current market trend (uptrend, downtrend, or horizontal)
    by analyzing various indicators such as ADX, DI, RSI, and ATR. It returns a string
    representing the trend ('uptrend', 'downtrend', 'horizontal', or 'none').

    Args:
        df (pandas.DataFrame): The DataFrame containing the market data.
        hunter_settings (object): The settings for the bot, including the thresholds for trend identification.

    Returns:
        str: The market trend ('uptrend', 'downtrend', 'horizontal', or 'none').
    """
    latest_data = df.iloc[-1]
    
    avg_adx_period = hunter_settings.avg_adx_period
    avg_adx = df['adx'].iloc[-avg_adx_period:].mean()
    
    adx_trend = (
        float(latest_data['adx']) > float(hunter_settings.adx_strong_trend) or 
        float(latest_data['adx']) > float(avg_adx)
        )
    
    avg_di_period = hunter_settings.avg_di_period
    avg_plus_di = df['plus_di'].iloc[-avg_di_period:].mean()
    avg_minus_di = df['minus_di'].iloc[-avg_di_period:].mean()
    
    di_difference_increasing = (
        abs(float(latest_data['plus_di']) - float(latest_data['minus_di'])) > 
        abs(float(avg_plus_di) - float(avg_minus_di)))
    
    significant_move = (
        (float(latest_data['high']) - float(latest_data['low'])) > 
        float(latest_data['atr']))
    
    is_rsi_bullish = float(latest_data['rsi']) < float(hunter_settings.rsi_sell)
    is_rsi_bearish = float(latest_data['rsi']) > float(hunter_settings.rsi_buy)
    
    is_strong_plus_di = float(latest_data['plus_di']) > float(hunter_settings.adx_weak_trend)
    is_strong_minus_di = float(latest_data['minus_di']) > float(hunter_settings.adx_weak_trend)

    uptrend = (
        is_rsi_bullish and 
        adx_trend and 
        di_difference_increasing and 
        is_strong_plus_di and 
        significant_move and 
        float(latest_data['plus_di']) > float(avg_minus_di)
        )

    downtrend = (
        is_rsi_bearish and 
        adx_trend and 
        di_difference_increasing and 
        is_strong_minus_di and 
        significant_move and 
        float(latest_data['plus_di']) < float(avg_minus_di)
        )      

    horizontal = (
        float(latest_data['adx']) < avg_adx or 
        avg_adx < float(hunter_settings.adx_weak_trend) or 
        abs(float(latest_data['plus_di']) - float(latest_data['minus_di'])) < 
        float(hunter_settings.adx_no_trend)
    )

    if uptrend:
        logger.trade(f"Bot {hunter_settings.id} {hunter_settings.strategy} have BULLISH UPTREND")
        return 'uptrend'
    elif downtrend:
        logger.trade(f"Bot {hunter_settings.id} {hunter_settings.strategy} have BEARISH DOWNTREND")
        return 'downtrend'
    elif horizontal:
        logger.trade(f"Bot {hunter_settings.id} {hunter_settings.strategy} have HORIZONTAL TREND")
        return 'horizontal'