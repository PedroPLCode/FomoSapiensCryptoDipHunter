from datetime import timedelta
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from zen.utils.logging import logger
from zen.utils.exception_handlers import exception_handler
import plotly.graph_objects as go
import plotly.io as pio
import base64
from io import BytesIO

@exception_handler()
def plot_selected_ta_indicators(df, settings):
    """
    Generates an interactive Plotly chart with selected technical analysis indicators.
    """
    indicators = settings.selected_plot_indicators
    validate_indicators(df, indicators)
    
    if df.empty:
        print("DataFrame is empty, nothing to plot.")
        return None
    
    if settings.lookback is not None:
        lookback_duration = parse_lookback(settings.lookback)
        cutoff_time = df['open_time'].max() - lookback_duration
        df = df[df['open_time'] >= cutoff_time]
    
    fig = go.Figure()
    
    if 'close' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['close'], name='Close Price', line=dict(color='blue')))
    
    if 'ema' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ema_fast'], name='EMA Fast', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ema_slow'], name='EMA Slow', line=dict(color='red')))
    
    if 'ma_50' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ma_50'], name='MA50', line=dict(color='orange')))
    if 'ma_200' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ma_200'], name='MA200', line=dict(color='purple')))
    
    if 'macd' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['macd'], name='MACD', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['macd_signal'], name='MACD Signal', line=dict(color='orange')))
        fig.add_trace(go.Bar(x=df['open_time'], y=df['macd_histogram'], name='MACD Histogram', marker_color='grey'))
    
    if 'boll' in indicators:
        fig.add_trace(go.Scatter(
            x=df['open_time'], 
            y=df['upper_band'], 
            name='Upper Band', 
            line=dict(color='green')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['open_time'], 
            y=df['lower_band'], 
            name='Lower Band', 
            line=dict(color='red'), 
            fill='tonexty',  # Wypełnienie między liniami
            fillcolor='rgba(128, 128, 128, 0.2)'  # Kolor wypełnienia z przezroczystością
        ))

    if 'rsi' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['rsi'], name='RSI', line=dict(color='purple')))
        fig.add_shape(type="line",
                  x0=df['open_time'].min(), x1=df['open_time'].max(),
                  y0=settings.rsi_sell, y1=settings.rsi_sell,
                  line=dict(color="red", width=2, dash="dash"),
                  name="RSI Max")

        fig.add_shape(type="line",
                    x0=df['open_time'].min(), x1=df['open_time'].max(),
                    y0=settings.rsi_buy, y1=settings.rsi_buy,
                    line=dict(color="green", width=2, dash="dash"),
                    name="RSI Min")
        
    if 'atr' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['atr'], name='ATR', line=dict(color='blue')))
    
    if 'cci' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['cci'], name='CCI', line=dict(color='brown')))
        fig.add_shape(type="line",
                x0=df['open_time'].min(), x1=df['open_time'].max(),
                y0=settings.cci_sell, y1=settings.cci_sell,
                line=dict(color="red", width=2, dash="dash"),
                name="cci Max")

        fig.add_shape(type="line",
                    x0=df['open_time'].min(), x1=df['open_time'].max(),
                    y0=settings.cci_buy, y1=settings.cci_buy,
                    line=dict(color="green", width=2, dash="dash"),
                    name="cci Min")
    if 'mfi' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['mfi'], name='MFI', line=dict(color='orange')))
        fig.add_shape(type="line",
                  x0=df['open_time'].min(), x1=df['open_time'].max(),
                  y0=settings.mfi_sell, y1=settings.mfi_sell,
                  line=dict(color="red", width=2, dash="dash"),
                  name="mfi Max")

        fig.add_shape(type="line",
                    x0=df['open_time'].min(), x1=df['open_time'].max(),
                    y0=settings.mfi_buy, y1=settings.mfi_buy,
                    line=dict(color="green", width=2, dash="dash"),
                    name="mfi Min")
    if 'stoch' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['stoch_k'], name='Stoch %K', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['stoch_d'], name='Stoch %D', line=dict(color='orange')))
    
    if 'stoch_rsi' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['stoch_rsi_k'], name='Stoch RSI %K', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['stoch_rsi_d'], name='Stoch RSI %D', line=dict(color='orange')))
    
    if 'psar' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['psar'], name='PSAR', mode='markers', marker=dict(color='red')))
    
    if 'vwap' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['vwap'], name='VWAP', mode='markers', marker=dict(color='red')))
    
    if 'adx' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['adx'], name='ADX', line=dict(color='purple')))
    
    if 'di' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['plus_di'], name='+DI', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['minus_di'], name='-DI', line=dict(color='red')))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        #autosize=True,
        width=1000,  # Szerokość wykresu
        height=800,  # Wysokość wykresu
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_visible=False,
        yaxis_visible=False,
    )
    
    img = BytesIO()
    pio.write_image(fig, img, format='png')
    img.seek(0)
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