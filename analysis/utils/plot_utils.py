from datetime import timedelta
import re
import matplotlib

matplotlib.use("Agg")
from io import BytesIO
import base64
from fomo_sapiens.utils.exception_handlers import exception_handler
from analysis.utils.calc_utils import is_df_valid
import plotly.graph_objects as go
import plotly.io as pio
import base64
from io import BytesIO
import pandas as pd
from typing import List, Optional, Union


@exception_handler(default_return=None)
def plot_selected_ta_indicators(df: pd.DataFrame, settings: object) -> Optional[str]:
    """
    Generates an interactive Plotly chart with selected technical analysis indicators.

    This function creates a chart that visualizes various technical analysis indicators based on the given DataFrame
    and user settings. It validates the indicators, filters the data if necessary, and generates the plot with relevant
    traces (e.g., price, moving averages, RSI, MACD).

    Parameters:
        df (DataFrame): The DataFrame containing the trading data.
        settings (object): The settings object containing user-selected indicators and chart configurations.

    Returns:
        str: A base64-encoded PNG image of the chart.
    """
    selected_indicators = getattr(settings, "selected_plot_indicators", None)
    if selected_indicators:
        indicators = prepare_selected_indicators_list(selected_indicators)
    else:
        indicators = get_bot_specific_plot_indicators(settings) or ["rsi", "macd"]

    validate_indicators(df, indicators)
    if not is_df_valid(df):
        return None

    min_bars_required = get_min_bars_required(indicators)

    if settings.lookback is not None:
        lookback_duration = parse_lookback(settings.lookback)
        cutoff_time = df["open_time"].max() - lookback_duration
        df = df[df["open_time"] >= cutoff_time]

    if len(df) < min_bars_required:
        df = df.tail(min_bars_required)
    elif len(df) > min_bars_required:
        extra_bars_needed = min_bars_required
        df = df.tail(len(df) + extra_bars_needed)

    fig = go.Figure()
    add_price_traces(fig, df, indicators)
    add_ta_traces(fig, df, indicators, settings)
    format_chart(fig)

    return generate_plot_image(fig)


@exception_handler()
def get_min_bars_required(indicators: list) -> int:
    """
    Returns the minimum number of bars required to properly calculate all selected indicators.
    """
    indicator_requirements = {
        "ma200": 200,
        "ma50": 50,
        "ema": 50,
        "rsi": 14,
        "macd": 26,
        "boll": 20,
        "atr": 14,
        "cci": 20,
        "mfi": 14,
        "stoch": 14,
        "stoch_rsi": 14,
        "psar": 5,
        "vwap": 1,
        "adx": 14,
        "di": 14,
        "close": 1,
    }

    return max([indicator_requirements.get(ind, 0) for ind in indicators])


@exception_handler(default_return=False)
def add_price_traces(fig: go.Figure, df: pd.DataFrame, indicators: List[str]) -> None:
    """
    Adds traces for price data to the Plotly figure.

    This function adds traces to the figure for various price-related indicators like 'close', 'ema', 'ma50', and 'ma200',
    based on the selected indicators.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure object to which traces are added.
        df (DataFrame): The DataFrame containing the data for the price traces.
        indicators (list): The list of selected indicators to plot.

    Returns:
        None
    """
    if "close" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df["close"],
                name="Close Price",
                line=dict(color="blue"),
            )
        )
    if "ema" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df["ema_fast"],
                name="EMA Fast",
                line=dict(color="green"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df["ema_slow"],
                name="EMA Slow",
                line=dict(color="red"),
            )
        )
    if "ma50" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"], y=df["ma_50"], name="MA50", line=dict(color="orange")
            )
        )
    if "ma200" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df["ma_200"],
                name="MA200",
                line=dict(color="purple"),
            )
        )


@exception_handler(default_return=False)
def add_ta_traces(
    fig: go.Figure, df: pd.DataFrame, indicators: List[str], settings: object
) -> None:
    """
    Adds traces for various technical analysis indicators to the Plotly figure.

    This function checks which technical analysis indicators are selected and adds their respective traces to the figure.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure object to which traces are added.
        df (DataFrame): The DataFrame containing the data for the indicators.
        indicators (list): The list of selected indicators to plot.
        settings (object): The settings object containing configuration values for indicators.

    Returns:
        None
    """
    ta_mappings = {
        "macd": [
            ("macd", "blue"),
            ("macd_signal", "orange"),
            ("macd_histogram", "grey", "lines"),
        ],
        "boll": [
            ("upper_band", "green"),
            ("lower_band", "red"),
            ("middle_band", "yellow"),
        ],
        "rsi": [
            (
                "rsi",
                "purple",
                None,
                None,
                [(settings.rsi_sell, "red"), (settings.rsi_buy, "green")],
            )
        ],
        "cci": [
            (
                "cci",
                "brown",
                None,
                None,
                [(settings.cci_sell, "red"), (settings.cci_buy, "green")],
            )
        ],
        "mfi": [
            (
                "mfi",
                "orange",
                None,
                None,
                [(settings.mfi_sell, "red"), (settings.mfi_buy, "green")],
            )
        ],
        "stoch": [("stoch_k", "blue"), ("stoch_d", "orange")],
        "stoch_rsi": [("stoch_rsi_k", "blue"), ("stoch_rsi_d", "orange")],
        "psar": [("psar", "red", "markers")],
        "vwap": [("vwap", "red", "markers")],
        "adx": [("adx", "purple")],
        "atr": [("atr", "purple")],
        "di": [("plus_di", "green"), ("minus_di", "red")],
    }

    for indicator, traces in ta_mappings.items():
        if indicator in indicators:
            for trace in traces:
                add_trace(fig, df, *trace)


@exception_handler(default_return=False)
def add_trace(
    fig: go.Figure,
    df: pd.DataFrame,
    column: str,
    color: str,
    mode: str = "lines",
    fillcolor: Optional[str] = None,
    horizontal_lines: Optional[List[tuple]] = None,
) -> None:
    """
    Adds a single trace to the Plotly figure.

    This function adds a trace for the specified column in the DataFrame to the Plotly figure, with optional configurations
    for line mode, fill color, and horizontal lines.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure object to which the trace is added.
        df (DataFrame): The DataFrame containing the data for the trace.
        column (str): The column name in the DataFrame to plot.
        color (str): The color for the line in the plot.
        mode (str, optional): The mode for the line, default is 'lines'.
        fillcolor (str, optional): The fill color for the area under the line.
        horizontal_lines (list, optional): A list of horizontal lines to add to the plot.

    Returns:
        None
    """
    if column in df:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df[column],
                name=column.upper(),
                line=dict(color=color),
                mode=mode,
            )
        )

    if fillcolor:
        fig.add_trace(
            go.Scatter(
                x=df["open_time"],
                y=df[column],
                fill="tonexty",
                fillcolor=fillcolor,
                line=dict(color=color),
            )
        )

    if horizontal_lines:
        for y_val, h_color in horizontal_lines:
            fig.add_shape(
                type="line",
                x0=df["open_time"].min(),
                x1=df["open_time"].max(),
                y0=y_val,
                y1=y_val,
                line=dict(color=h_color, width=2, dash="dash"),
            )


@exception_handler(default_return=False)
def format_chart(fig: go.Figure) -> None:
    """
    Applies formatting to the Plotly figure.

    This function sets the layout options for the figure, such as background color, grid visibility, and axis properties.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure object to format.

    Returns:
        None
    """
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
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
            font=dict(size=26),
        ),
        xaxis=dict(tickfont=dict(size=26)),
        yaxis=dict(tickfont=dict(size=26)),
    )


@exception_handler(default_return=None)
def generate_plot_image(fig: go.Figure) -> Optional[str]:
    """
    Converts the Plotly figure into a base64-encoded PNG image.

    This function generates a PNG image of the Plotly figure and encodes it into base64 format to be used in web pages or APIs.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure to convert into an image.

    Returns:
        str: A base64-encoded PNG image.
    """
    img = BytesIO()
    pio.write_image(fig, img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")


@exception_handler(default_return=False)
def parse_lookback(lookback: str) -> timedelta:
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

            if unit == "d":
                return timedelta(days=value)
            elif unit == "h":
                return timedelta(hours=value)
            elif unit == "m":
                return timedelta(minutes=value)
            elif unit == "s":
                return timedelta(seconds=value)
            elif unit == "w":
                return timedelta(days=value * 7)
            elif unit == "M":
                return timedelta(days=value * 30)
            else:
                raise ValueError(f"Unknown time unit: {unit}")
        else:
            raise ValueError(f"Invalid lookback format: {lookback}")
    else:
        raise TypeError("Lookback must be a string in the format 'Xd', 'Xh', or 'Xm'.")


@exception_handler(default_return=False)
def validate_indicators(df: pd.DataFrame, indicators: List[str]) -> None:
    """
    Validates that the required columns for the selected indicators are present in the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        indicators (list): The list of indicators to validate.

    Returns:
        None
    """
    required_columns = {
        "close": ["close"],
        "volume": ["volume"],
        "ema": ["ema_fast", "ema_slow"],
        "ma50": ["ma_50"],
        "ma200": ["ma_200"],
        "macd": ["macd", "macd_signal", "macd_histogram"],
        "boll": ["upper_band", "lower_band"],
        "rsi": ["rsi"],
        "atr": ["atr"],
        "cci": ["cci"],
        "mfi": ["mfi"],
        "stoch": ["stoch_k", "stoch_d"],
        "stoch_rsi": ["stoch_rsi_k", "stoch_rsi_d"],
        "psar": ["psar"],
        "vwap": ["vwap"],
        "adx": ["adx"],
        "di": ["plus_di", "minus_di"],
    }

    for indicator in indicators:
        if indicator in required_columns:
            missing_columns = [
                col for col in required_columns[indicator] if col not in df.columns
            ]
            if missing_columns:
                raise ValueError(
                    f"Missing required columns for indicator {indicator}: {', '.join(missing_columns)}"
                )
        else:
            raise ValueError(f"Unknown indicator: {indicator}")


def prepare_selected_indicators_list(
    indicators_list: Union[str, List[str]],
) -> List[str]:
    """
    Prepares and returns a list of selected indicators by parsing a comma-separated string
    or returning the given list of indicators. Each indicator is stripped of any leading
    or trailing whitespace.

    Parameters:
        indicators_list (str or list): A string of comma-separated indicators or a list of indicators.

    Returns:
        list: A list of indicator strings.

    Raises:
        ValueError: If the input is neither a string nor a list.
    """
    if isinstance(indicators_list, str):
        return [indicator.strip() for indicator in indicators_list.split(",")]
    elif isinstance(indicators_list, list):
        return [indicator.strip() for indicator in indicators_list]
    else:
        raise ValueError("Input should be a string or a list")


@exception_handler()
def get_bot_specific_plot_indicators(settings) -> List[str]:
    """
    Extracts and returns a list of selected trading indicators based on the given settings
    that determine which indicators should be plotted.

    Parameters:
        settings (object): An object containing boolean attributes that determine which indicators
                          are selected for plotting. Each attribute corresponds to a specific indicator.

    Returns:
        list: A list of strings representing the selected indicators, such as 'rsi', 'macd', 'boll', etc.
    """
    indicators = []

    if settings.price_signals:
        indicators.append("close")
    if settings.rsi_signals or settings.rsi_divergence_signals:
        indicators.append("rsi")
    if settings.cci_signals or settings.cci_divergence_signals:
        indicators.append("cci")
    if settings.mfi_signals or settings.mfi_divergence_signals:
        indicators.append("mfi")
    if settings.macd_cross_signals or settings.macd_histogram_signals:
        indicators.append("macd")
    if settings.bollinger_signals:
        indicators.append("boll")
    if settings.stoch_signals or settings.stoch_divergence_signals:
        indicators.append("stoch")
    if settings.stoch_rsi_signals:
        indicators.append("stoch_rsi")
    if (
        settings.ema_cross_signals
        or settings.ema_fast_signals
        or settings.ema_slow_signals
    ):
        indicators.append("ema")
    if settings.di_signals:
        indicators.append("di")
    if settings.atr_signals:
        indicators.append("atr")
    if settings.vwap_signals:
        indicators.append("vwap")
    if settings.psar_signals:
        indicators.append("psar")
    if settings.ma50_signals or settings.ma_cross_signals:
        indicators.append("ma50")
    if settings.ma200_signals or settings.ma_cross_signals:
        indicators.append("ma200")
    if settings.trend_signals:
        indicators.append("adx")

    return indicators
