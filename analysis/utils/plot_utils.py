from datetime import timedelta
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from FomoSapiensCryptoDipHunter.utils.logging import logger
from FomoSapiensCryptoDipHunter.utils.exception_handlers import exception_handler
import plotly.graph_objects as go
import plotly.io as pio
import base64
from io import BytesIO

@exception_handler(default_return=None)
def plot_selected_ta_indicators(df, settings):
    """
    Generates an interactive Plotly chart with selected technical analysis indicators.
    """
    indicators = prepare_selected_indicators_list(settings.selected_plot_indicators)
    validate_indicators(df, indicators)
    
    if df.empty:
        print("DataFrame is empty, nothing to plot.")
        return None
    
    if settings.lookback is not None:
        lookback_duration = parse_lookback(settings.lookback)
        cutoff_time = df['open_time'].max() - lookback_duration
        df = df[df['open_time'] >= cutoff_time]
    
    fig = go.Figure()
    add_price_traces(fig, df, indicators)
    add_ta_traces(fig, df, indicators, settings)
    format_chart(fig)
    
    return generate_plot_image(fig)

@exception_handler(default_return=False)
def add_price_traces(fig, df, indicators):
    """Adds price-related traces to the figure."""
    if 'close' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['close'], name='Close Price', line=dict(color='blue')))
    if 'ema' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ema_fast'], name='EMA Fast', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ema_slow'], name='EMA Slow', line=dict(color='red')))
    if 'ma_50' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ma_50'], name='MA50', line=dict(color='orange')))
    if 'ma_200' in indicators:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df['ma_200'], name='MA200', line=dict(color='purple')))


@exception_handler(default_return=False)
def add_ta_traces(fig, df, indicators, settings):
    """Adds technical analysis indicator traces to the figure."""
    ta_mappings = {
        'macd': [('macd', 'blue'), ('macd_signal', 'orange'), ('macd_histogram', 'grey', 'lines')],
        'boll': [('upper_band', 'green'), ('lower_band', 'red', None, 'rgba(128, 128, 128, 0.2)')],
        'rsi': [('rsi', 'purple', None, None, [(settings.rsi_sell, 'red'), (settings.rsi_buy, 'green')])],
        'cci': [('cci', 'brown', None, None, [(settings.cci_sell, 'red'), (settings.cci_buy, 'green')])],
        'mfi': [('mfi', 'orange', None, None, [(settings.mfi_sell, 'red'), (settings.mfi_buy, 'green')])],
        'stoch': [('stoch_k', 'blue'), ('stoch_d', 'orange')],
        'stoch_rsi': [('stoch_rsi_k', 'blue'), ('stoch_rsi_d', 'orange')],
        'psar': [('psar', 'red', 'markers')],
        'vwap': [('vwap', 'red', 'markers')],
        'adx': [('adx', 'purple')],
        'atr': [('atr', 'purple')],
        'di': [('plus_di', 'green'), ('minus_di', 'red')]
    }
    
    for indicator, traces in ta_mappings.items():
        if indicator in indicators:
            for trace in traces:
                add_trace(fig, df, *trace)


@exception_handler(default_return=False)
def add_trace(fig, df, column, color, mode='lines', fillcolor=None, horizontal_lines=None):
    """Adds a single trace to the figure."""
    if column in df:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df[column], name=column.upper(), line=dict(color=color), mode=mode))
    
    if fillcolor:
        fig.add_trace(go.Scatter(x=df['open_time'], y=df[column], fill='tonexty', fillcolor=fillcolor, line=dict(color=color)))
    
    if horizontal_lines:
        for y_val, h_color in horizontal_lines:
            fig.add_shape(type="line", x0=df['open_time'].min(), x1=df['open_time'].max(), y0=y_val, y1=y_val,
                          line=dict(color=h_color, width=2, dash="dash"))


@exception_handler(default_return=False)
def format_chart(fig):
    """Applies formatting to the figure."""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=1000,
        height=800,
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_visible=True,
        yaxis_visible=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5,
            font=dict(
                size=26
            )
        ),
        xaxis=dict(
            tickfont=dict(
                size=26
            )
        ),
        yaxis=dict(
            tickfont=dict(
                size=26
            )
        )
    )


@exception_handler(default_return=None)
def generate_plot_image(fig):
    """Generates a base64-encoded PNG image from the figure."""
    img = BytesIO()
    pio.write_image(fig, img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')


@exception_handler(default_return=False)
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


@exception_handler(default_return=False)
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
        'stoch_rsi': ['stoch_rsi_k', 'stoch_rsi_d'],
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
        
        
def prepare_selected_indicators_list(indicators_list):
    return [indicator.strip() for indicator in indicators_list.split(',')]