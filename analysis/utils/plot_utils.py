from datetime import timedelta
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from DipHunterCryptoTechnicalAnalysis.utils.logging import logger
from DipHunterCryptoTechnicalAnalysis.utils.exception_handlers import exception_handler

@exception_handler()
def plot_selected_ta_indicators(
    df, 
    settings, 
    lookback=None
    ):
    """
    Plots selected technical analysis indicators on a chart, such as moving averages, RSI, MACD, and others.

    Parameters:
        df (DataFrame): The DataFrame containing the historical market data.
        indicators (list): List of indicators to plot (e.g., ['close', 'ema', 'rsi']).
        bot_settings (object): The bot's configuration settings containing thresholds for indicators like RSI and CCI.
        lookback (str, optional): The time period for filtering data, such as '10d' for 10 days.

    Returns:
        str: A base64 encoded image URL of the generated plot, or None if an error occurs.
    """
    indicators = settings.selected_plot_indicators
    validate_indicators(df, indicators)
    
    if df.empty:
        print("DataFrame is empty, nothing to plot.")
        return None

    if lookback is not None:
        lookback_duration = parse_lookback(lookback)
        cutoff_time = df['open_time'].max() - lookback_duration
        df = df[df['open_time'] >= cutoff_time]
        
    fig, ax = plt.subplots(figsize=(14, 10))
    ax2 = ax.twinx()
    linw_width = 4
    dot_size = 24

    if 'close' in indicators:
        ax.plot(df['open_time'], df['close'], label='Close Price', color='blue', linewidth=linw_width)

    if 'ema' in indicators:
        ax.plot(df['open_time'], df['ema_fast'], label='EMA Fast', color='green', linewidth=linw_width)
        ax.plot(df['open_time'], df['ema_slow'], label='EMA Slow', color='red', linewidth=linw_width)
    
    if 'ma50' in indicators:
        ax.plot(df['open_time'], df['ma_50'], label='MA50', color='orange', linewidth=linw_width)
    if 'ma200' in indicators:
        ax.plot(df['open_time'], df['ma_200'], label='MA200', color='purple', linewidth=linw_width)

    if 'macd' in indicators:
        ax.plot(df['open_time'], df['macd'], label='MACD', color='blue', linewidth=linw_width)
        ax.plot(df['open_time'], df['macd_signal'], label='MACD Signal', color='orange', linewidth=linw_width)
        ax.bar(df['open_time'], df['macd_histogram'], label='MACD Histogram', color='grey', alpha=0.5)

    if 'boll' in indicators:
        ax.plot(df['open_time'], df['upper_band'], label='Upper Band', color='green', linewidth=linw_width)
        ax.plot(df['open_time'], df['lower_band'], label='Lower Band', color='red', linewidth=linw_width)
        ax.fill_between(df['open_time'], df['lower_band'], df['upper_band'], color='grey', alpha=0.2)

    if 'rsi' in indicators:
        ax2.plot(df['open_time'], df['rsi'], label='RSI', color='purple', linewidth=linw_width)
        ax2.axhline(y=settings.rsi_sell, color='red', linestyle='--', linewidth=linw_width)
        ax2.axhline(y=settings.rsi_buy, color='green', linestyle='--', linewidth=linw_width)

    if 'atr' in indicators:
        ax.plot(df['open_time'], df['atr'], label='ATR', color='blue', linewidth=linw_width)

    if 'cci' in indicators:
        ax2.plot(df['open_time'], df['cci'], label='CCI', color='brown', linewidth=linw_width)
        ax2.axhline(y=settings.cci_sell, color='red', linestyle='--', linewidth=linw_width)
        ax2.axhline(y=settings.cci_buy, color='green', linestyle='--', linewidth=linw_width)

    if 'mfi' in indicators:
        ax2.plot(df['open_time'], df['mfi'], label='MFI', color='orange', linewidth=linw_width)
        ax2.axhline(y=settings.mfi_sell, color='red', linestyle='--', linewidth=linw_width)
        ax2.axhline(y=settings.mfi_buy, color='green', linestyle='--', linewidth=linw_width)

    if 'stoch' in indicators:
        ax.plot(df['open_time'], df['stoch_k'], label='Stoch %K', color='blue', linewidth=linw_width)
        ax.plot(df['open_time'], df['stoch_d'], label='Stoch %D', color='orange', linewidth=linw_width)

    if 'st_rsi' in indicators:
        ax.plot(df['open_time'], df['stoch_rsi_k'], label='Stoch RSI %K', color='blue', linewidth=linw_width)
        ax.plot(df['open_time'], df['stoch_rsi_d'], label='Stoch RSI %D', color='orange', linewidth=linw_width)

    if 'psar' in indicators:
        ax.scatter(df['open_time'], df['psar'], label='PSAR', color='red', s=dot_size)

    if 'vwap' in indicators:
        ax.scatter(df['open_time'], df['vwap'], label='VWAP', color='red', s=dot_size)

    if 'adx' in indicators:
        ax.plot(df['open_time'], df['adx'], label='ADX', color='purple', linewidth=linw_width)
    
    if 'di' in indicators:
        ax.plot(df['open_time'], df['plus_di'], label='+DI', color='green', linewidth=linw_width)
        ax.plot(df['open_time'], df['minus_di'], label='-DI', color='red', linewidth=linw_width)

    ax.legend(loc='upper left', prop={'size': 42})
    ax2.legend(loc='lower left', prop={'size': 42})
    
    ax.set_xticks([])
    ax.set_yticks([])

    ax2.set_xticks([])
    ax2.set_yticks([])

    plt.tight_layout()
    
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close(fig)

    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return plot_url


@exception_handler()
def parse_lookback(lookback):
    """
    Parses a lookback period string (e.g., '10d', '3h', '5m') into a timedelta object.

    Parameters:
        lookback (str): The lookback period in a string format, such as '10d', '3h', '5m'.

    Returns:
        timedelta: The corresponding timedelta object representing the lookback period.
    """
    if isinstance(lookback, str):
        match = re.match(r"(\d+)([a-zA-Z]+)", lookback)
        if match:
            value, unit = match.groups()
            value = int(value)
            if unit == 'd':
                return timedelta(days=value)
            elif unit == 'h':
                return timedelta(hours=value)
            elif unit == 'm':
                return timedelta(minutes=value)
            elif unit == 's':
                return timedelta(seconds=value)
            else:
                raise ValueError(f"Unknown time unit: {unit}")
        else:
            raise ValueError(f"Invalid lookback format: {lookback}")
    else:
        raise TypeError("Lookback must be a string in the format 'Xd', 'Xh', or 'Xm'.")


@exception_handler()
def validate_indicators(df, indicators):
    """
    Validates that the required columns for the selected indicators are present in the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the data to be validated.
        indicators (list): The list of indicators to validate.

    Raises:
        ValueError: If any required columns for the selected indicators are missing in the DataFrame.
    """ 
    required_columns = {
        'close': ['close'],
        'ema': ['ema_fast', 'ema_slow'],
        'ma50': ['ma_50'],
        'ma200': ['ma_200'],
        'macd': ['macd', 'macd_signal', 'macd_histogram'],
        'boll': ['upper_band', 'lower_band'],
        'rsi': ['rsi'],
        'atr': ['atr'],
        'cci': ['cci'],
        'mfi': ['mfi'],
        'stoch': ['stoch_k', 'stoch_d'],
        'st_rsi': ['stoch_rsi_k', 'stoch_rsi_d'],
        'psar': ['psar'],
        'vwap': ['vwap'],
        'adx': ['adx'],
        'di': ['plus_di', 'minus_di'],
    }

    for indicator in indicators:
        if indicator in required_columns:
            missing_columns = [col for col in required_columns[indicator] if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns for indicator {indicator}: {', '.join(missing_columns)}")
        else:
            raise ValueError(f"Unknown indicator: {indicator}")