import talib
import pandas as pd
from zen.utils.logging import logger
from zen.utils.exception_handlers import exception_handler

@exception_handler(default_return=False)
def handle_ta_df_initial_praparation(df, user_settings):
    """
    Prepares the DataFrame for technical analysis by converting relevant columns to numeric 
    types and handling missing values.

    Args:
        df (pandas.DataFrame): The raw DataFrame containing market data.
        user_settings (object): The bot's settings containing configuration for analysis.

    Returns:
        pandas.DataFrame: The cleaned DataFrame with numeric conversion and missing values handled.
        bool: False if an error occurs.
    """
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    
    df.dropna(subset=['close'], inplace=True)
    
    return df


@exception_handler(default_return=False)
def calculate_ta_rsi(df, user_settings):
    """
    Calculates the Relative Strength Index (RSI) using the 'close' price.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing RSI time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the RSI values added.
        bool: False if an error occurs.
    """
    df['rsi'] = talib.RSI(
        df['close'], 
        timeperiod=user_settings.rsi_timeperiod
        )
    
    return df
        

@exception_handler(default_return=False)
def calculate_ta_cci(df, user_settings):
    """
    Calculates the Commodity Channel Index (CCI) using 'high', 'low', and 'close' prices.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing CCI time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the CCI values added.
        bool: False if an error occurs.
    """
    df['cci'] = talib.CCI(
        df['high'],
        df['low'],
        df['close'],
        timeperiod=user_settings.cci_timeperiod
        )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_mfi(df, user_settings):
    """
    Calculates the Money Flow Index (MFI) using 'high', 'low', 'close', and 'volume' data.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing MFI time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the MFI values added.
        bool: False if an error occurs.
    """
    df['mfi'] = talib.MFI(
        df['high'],
        df['low'],
        df['close'],
        df['volume'],
        timeperiod=user_settings.mfi_timeperiod
        )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_adx(df, user_settings):
    """
    Calculates the Average Directional Index (ADX) using 'high', 'low', and 'close' prices.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing ADX time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the ADX values added.
        bool: False if an error occurs.
    """

    df['adx'] = talib.ADX(
        df['high'],
        df['low'],
        df['close'],
        timeperiod=user_settings.adx_timeperiod
        )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_atr(df, user_settings):
    """
    Calculates the Average True Range (ATR) using 'high', 'low', and 'close' prices.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing ATR time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the ATR values added.
        bool: False if an error occurs.
    """
    df['atr'] = talib.ATR(
        df['high'],
        df['low'],
        df['close'],
        timeperiod=user_settings.atr_timeperiod
        )
    
    return df
    

@exception_handler(default_return=False)
def calculate_ta_di(df, user_settings):
    """
    Calculates the Directional Indicators (DI) including the Plus DI and Minus DI 
    using 'high', 'low', and 'close' prices.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing DI time period configuration.

    Returns:
        pandas.DataFrame: The DataFrame with the Plus DI and Minus DI values added.
        bool: False if an error occurs.
    """
    df['plus_di'] = talib.PLUS_DI(
        df['high'],
        df['low'],
        df['close'],
        timeperiod=user_settings.di_timeperiod
        )
    
    df['minus_di'] = talib.MINUS_DI(
        df['high'],
        df['low'],
        df['close'],
        timeperiod=user_settings.di_timeperiod
        )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_stochastic(df, user_settings):
    """
    Calculates the Stochastic Oscillator using 'high', 'low', and 'close' prices.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing Stochastic parameters.

    Returns:
        pandas.DataFrame: The DataFrame with the Stochastic K and D values added.
        bool: False if an error occurs.
    """
    df['stoch_k'], df['stoch_d'] = talib.STOCH(
        df['high'],
        df['low'],
        df['close'],
        fastk_period=user_settings.stoch_k_timeperiod,
        slowk_period=user_settings.stoch_d_timeperiod,
        slowk_matype=0,
        slowd_period=user_settings.stoch_d_timeperiod,
        slowd_matype=0
    )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_bollinger_bands(df, user_settings):
    """
    Calculates the Bollinger Bands using 'close' price.

    Args:
        df (pandas.DataFrame): The DataFrame containing market data.
        user_settings (object): The bot's settings containing Bollinger Bands parameters.

    Returns:
        pandas.DataFrame: The DataFrame with the upper, middle, and lower bands added.
        bool: False if an error occurs.
    """
    df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(
        df['close'],
        timeperiod=user_settings.bollinger_timeperiod,
        nbdevup=user_settings.bollinger_nbdev,
        nbdevdn=user_settings.bollinger_nbdev,
        matype=0
    )
    
    return df


@exception_handler(default_return=False)
def calculate_ta_vwap(df, user_settings):
    """
    Calculate the Volume Weighted Average Price (VWAP) for the given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the price and volume data.
        user_settings (object): The bot settings object containing relevant configuration for the calculation.

    Returns:
        DataFrame: The original DataFrame with the calculated VWAP.
        bool: False if an error occurs during calculation.
    """
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['vwap'] = (df['typical_price'] * df['volume']).cumsum() / df['volume'].cumsum()
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_psar(df, user_settings):
    """
    Calculate the Parabolic SAR (PSAR) for the given DataFrame using bot settings.

    Args:
        df (DataFrame): The DataFrame containing the price data.
        user_settings (object): The bot settings object containing the acceleration and maximum values for PSAR calculation.

    Returns:
        DataFrame: The original DataFrame with the calculated PSAR.
        bool: False if an error occurs during calculation.
    """
    df['psar'] = talib.SAR(
        df['high'],
        df['low'],
        acceleration=user_settings.psar_acceleration,
        maximum=user_settings.psar_maximum
    )
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_macd(df, user_settings):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for the given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the closing price data.
        user_settings (object): The bot settings object containing configuration for MACD calculation.

    Returns:
        DataFrame: The original DataFrame with the calculated MACD and MACD signal.
        bool: False if not enough data points are available or if an error occurs.
    """
    if len(df) < user_settings.macd_timeperiod * 2:
        logger.trade('Not enough data points for MACD calculation.')
        return df
    
    df['macd'], df['macd_signal'], _ = talib.MACD(
        df['close'],
        fastperiod=user_settings.macd_timeperiod,
        slowperiod=user_settings.macd_timeperiod * 2,
        signalperiod=user_settings.macd_signalperiod
    )
    
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_ma(df, user_settings):
    """
    Calculate the 200-period and 50-period Moving Averages (MA) for the given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the closing price data.
        user_settings (object): The bot settings object (not used in this function).

    Returns:
        DataFrame: The original DataFrame with the calculated 200-period and 50-period MAs.
        bool: False if an error occurs during calculation.
    """
    df['ma_200'] = df['close'].rolling(window=200).mean()
    df['ma_50'] = df['close'].rolling(window=50).mean()
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_ema(df, user_settings):
    """
    Calculate the Fast and Slow Exponential Moving Averages (EMA) for the given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the closing price data.
        user_settings (object): The bot settings object containing the time periods for the fast and slow EMAs.

    Returns:
        DataFrame: The original DataFrame with the calculated fast and slow EMAs.
        bool: False if an error occurs during calculation.
    """
    df['ema_fast'] = talib.EMA(
        df['close'], 
        timeperiod=user_settings.ema_fast_timeperiod
        )
    
    df['ema_slow'] = talib.EMA(
        df['close'], 
        timeperiod=user_settings.ema_slow_timeperiod
        )
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_stochastic_rsi(df, user_settings):
    """
    Calculate the Stochastic RSI (Relative Strength Index) for the given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the RSI data.
        user_settings (object): The bot settings object containing the time periods for Stochastic RSI calculation.

    Returns:
        DataFrame: The original DataFrame with the calculated Stochastic RSI and its %K and %D values.
        bool: False if an error occurs during calculation.
    """
    df['stoch_rsi'] = talib.RSI(
        df['rsi'], 
        timeperiod=user_settings.stoch_rsi_timeperiod
        )
    
    df['stoch_rsi_k'], df['stoch_rsi_d'] = talib.STOCH(
        df['stoch_rsi'],
        df['stoch_rsi'],
        df['stoch_rsi'],
        fastk_period=user_settings.stoch_rsi_k_timeperiod,
        slowk_period=user_settings.stoch_rsi_d_timeperiod,
        slowk_matype=0,
        slowd_period=user_settings.stoch_rsi_d_timeperiod,
        slowd_matype=0
    )
    
    return df

    
@exception_handler(default_return=False)
def handle_ta_df_final_cleaning(df, columns_to_check, user_settings):
    """
    Clean the final DataFrame by removing rows with missing values in the specified columns.

    Args:
        df (DataFrame): The DataFrame to clean.
        columns_to_check (list): A list of column names to check for missing values.
        user_settings (object): The bot settings object (not used in this function).

    Returns:
        DataFrame: The cleaned DataFrame.
        bool: False if an error occurs during cleaning.
    """
    df[columns_to_check] = df[columns_to_check].fillna(0)
    
    return df

    
@exception_handler(default_return=False)
def calculate_ta_indicators(df, user_settings):
    """
    Calculates various technical analysis indicators on the given DataFrame.

    This function applies multiple technical indicators (RSI, CCI, MFI, etc.) to the input DataFrame
    and returns the updated DataFrame with the calculated values. It ensures the DataFrame is properly
    prepared and cleaned before returning the results.

    Args:
        df (pandas.DataFrame): The DataFrame containing the market data.
        user_settings (object): The settings for the bot, including parameters for the indicators.

    Returns:
        pandas.DataFrame: The updated DataFrame with calculated technical indicators, or False if an error occurs.
    """
    if df.empty:
        logger.error('DataFrame is empty, cannot calculate indicators.')
        return df

    handle_ta_df_initial_praparation(df, user_settings)

    calculate_ta_rsi(df, user_settings)
    calculate_ta_cci(df, user_settings)
    calculate_ta_mfi(df, user_settings)
    calculate_ta_stochastic(df, user_settings)
    calculate_ta_stochastic_rsi(df, user_settings)
    calculate_ta_bollinger_bands(df, user_settings)
    calculate_ta_ema(df, user_settings)
    calculate_ta_macd(df, user_settings)
    calculate_ta_ma(df, user_settings)
    calculate_ta_atr(df, user_settings)
    calculate_ta_psar(df, user_settings)
    calculate_ta_vwap(df, user_settings)
    calculate_ta_adx(df, user_settings)
    calculate_ta_di(df, user_settings)
    
    columns_to_check = []
    handle_ta_df_final_cleaning(df, columns_to_check, user_settings)

    return df


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