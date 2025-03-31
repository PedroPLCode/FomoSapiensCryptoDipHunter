from datetime import datetime as dt
from analysis.models import SentimentAnalysis
from analysis.utils.sentiment_utils import fetch_and_save_sentiment_analysis
from fomo_sapiens.utils.exception_handlers import exception_handler
import pandas as pd


@exception_handler()
def generate_ta_report_email(settings: object, df: pd.DataFrame) -> tuple[str, str]:
    """
    Generates an email report for technical analysis of a given symbol, interval, and lookback period.

    The function aggregates the latest and previous data, and computes various technical indicators,
    including RSI, CCI, MFI, MACD, Bollinger Bands, Stochastic Indicators, EMA, DMI, ATR, VWAP,
    Parabolic SAR, Moving Averages, and ADX, based on the provided settings. It then constructs an
    email subject and content with this information for further analysis.

    Parameters:
        settings (object): An object containing the settings related to the trading symbol,
                            indicators, and thresholds for various technical analysis parameters.
        df (DataFrame): A DataFrame containing the historical market data (e.g., OHLCV) to compute
                        technical indicators and trends.

    Returns:
        tuple: A tuple containing the subject (str) and content (str) of the email.
            - subject: A string subject for the email report.
            - content: A string with detailed information about the technical analysis,
              including the latest and previous data, technical indicators, and trend.
    """
    from hunter.utils.hunter_logic import get_latest_and_previus_data

    now = dt.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    time: dt = settings.df_last_fetch_time
    formatted_time: str = time.strftime("%Y-%m-%d %H:%M:%S")
    latest_data, previous_data = get_latest_and_previus_data(df)

    sentiment_analysis = SentimentAnalysis.objects.filter(id=1).first()

    if not sentiment_analysis:
        fetch_and_save_sentiment_analysis()
        sentiment_analysis = SentimentAnalysis.objects.filter(id=1).first()

    sentiment_last_update = (
        sentiment_analysis.sentiment_last_update_time.strftime("%Y-%m-%d %H:%M:%S")
        if sentiment_analysis
        else None
    )

    subject: str = "Technical Analysis report."

    content: str = (
        f"FomoSapiensCryptoDipHunter\n"
        f"https://fomo.ropeaccess.pro\n\n"
        f"Overall Sentiment Analysis.\n"
        f"{sentiment_last_update}\n"
        f"Current Sentiment: {sentiment_analysis.sentiment_score:.2f} {sentiment_analysis.sentiment_label}\n\n"
        f"Technical Analysis report.\n"
        f"{formatted_now}\n\n"
        f"Technical Analysis data:\n"
        f"symbol: {settings.symbol}\n"
        f"interval: {settings.interval}\n"
        f"lookback: {settings.lookback}\n"
        f"df_last_fetch_time: {formatted_time}\n\n"
        f"Technical Analysis details:\n\n"
        f"open_time: {latest_data['open_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"close_time: {latest_data['close_time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"close_latest_data: {latest_data['close']:.2f}\n"
        f"close_previous_data: {previous_data['close']:.2f}\n\n"
        f"volume_latest_data: {latest_data['volume']:.2f}\n"
        f"volume_previous_data: {previous_data['volume']:.2f}\n\n"
        "RSI (Relative Strength Index):\n"
        f"rsi_timeperiod: {settings.rsi_timeperiod}\n"
        f"rsi_latest_data: {latest_data['rsi']:.2f}\n"
        f"rsi_previous_data: {previous_data['rsi']:.2f}\n"
        f"rsi_buy: {settings.rsi_buy}\n"
        f"rsi_sell: {settings.rsi_sell}\n\n"
        "CCI (Commodity Channel Index):\n"
        f"cci_timeperiod: {settings.cci_timeperiod}\n"
        f"cci_latest_data: {latest_data['cci']:.2f}\n"
        f"cci_previous_data: {previous_data['cci']:.2f}\n"
        f"cci_buy: {settings.cci_buy}\n"
        f"cci_sell: {settings.cci_sell}\n\n"
        "MFI (Money Flow Index):\n"
        f"mfi_timeperiod: {settings.mfi_timeperiod}\n"
        f"mfi_latest_data: {latest_data['mfi']:.2f}\n"
        f"mfi_previous_data: {previous_data['mfi']:.2f}\n"
        f"mfi_buy: {settings.mfi_buy}\n"
        f"mfi_sell: {settings.mfi_sell}\n\n"
        "MACD (Moving Average Convergence Divergence):\n"
        f"macd_timeperiod: {settings.macd_timeperiod}\n"
        f"macd_signalperiod: {settings.macd_signalperiod}\n"
        f"macd_latest_data: {latest_data['macd']:.2f}\n"
        f"macd_signal_latest_data: {latest_data['macd_signal']:.2f}\n"
        f"macd_previous_data: {previous_data['macd']:.2f}\n"
        f"macd_signal_previous_data: {previous_data['macd_signal']:.2f}\n\n"
        "Bollinger Bands:\n"
        f"bollinger_timeperiod: {settings.bollinger_timeperiod}\n"
        f"bollinger_nbdev: {settings.bollinger_nbdev}\n"
        f"upper_band_latest_data: {latest_data['upper_band']:.2f}\n"
        f"middle_band_latest_data: {latest_data['middle_band']:.2f}\n"
        f"lower_band_latest_data: {latest_data['lower_band']:.2f}\n"
        f"upper_band_previous_data: {previous_data['upper_band']:.2f}\n"
        f"middle_band_previous_data: {previous_data['middle_band']:.2f}\n"
        f"lower_band_previous_data: {previous_data['lower_band']:.2f}\n\n"
        "Stochastic Indicators:\n"
        f"stoch_k_timeperiod: {settings.stoch_k_timeperiod}\n"
        f"stoch_d_timeperiod: {settings.stoch_d_timeperiod}\n"
        f"stoch_k_latest_data: {latest_data['stoch_k']:.2f}\n"
        f"stoch_d_latest_data: {latest_data['stoch_d']:.2f}\n"
        f"stoch_k_previous_data: {previous_data['stoch_k']:.2f}\n"
        f"stoch_d_previous_data: {previous_data['stoch_d']:.2f}\n"
        f"stoch_buy: {settings.stoch_buy}\n"
        f"stoch_sell: {settings.stoch_sell}\n\n"
        "Stochastic RSI Indicators:\n"
        f"stoch_rsi_timeperiod: {settings.stoch_rsi_timeperiod}\n"
        f"stoch_rsi_k_timeperiod: {settings.stoch_rsi_k_timeperiod}\n"
        f"stoch_rsi_d_timeperiod: {settings.stoch_rsi_d_timeperiod}\n"
        f"stoch_rsi_d_latest_data: {latest_data['stoch_rsi_d']:.2f}\n"
        f"stoch_rsi_k_latest_data: {latest_data['stoch_rsi_k']:.2f}\n"
        f"stoch_rsi_d_previous_data: {previous_data['stoch_rsi_d']:.2f}\n"
        f"stoch_rsi_k_previous_data: {previous_data['stoch_rsi_k']:.2f}\n\n"
        "EMA (Exponential Moving Averages):\n"
        f"ema_fast_timeperiod: {settings.ema_fast_timeperiod}\n"
        f"ema_slow_timeperiod: {settings.ema_slow_timeperiod}\n"
        f"ema_fast_latest_data: {latest_data['ema_fast']:.2f}\n"
        f"ema_slow_latest_data: {latest_data['ema_slow']:.2f}\n"
        f"ema_fast_previous_data: {previous_data['ema_fast']:.2f}\n"
        f"ema_slow_previous_data: {previous_data['ema_slow']:.2f}\n\n"
        "Directional Movement Index (DMI):\n"
        f"di_timeperiod: {settings.di_timeperiod}\n"
        f"plus_di_latest_data: {latest_data['plus_di']:.2f}\n"
        f"minus_di_latest_data: {latest_data['minus_di']:.2f}\n"
        f"plus_di_previous_data: {previous_data['plus_di']:.2f}\n"
        f"minus_di_previous_data: {previous_data['minus_di']:.2f}\n\n"
        "ATR (Average True Range):\n"
        f"atr_timeperiod: {settings.atr_timeperiod}\n"
        f"atr_latest_data: {latest_data['atr']:.2f}\n"
        f"atr_previous_data: {previous_data['atr']:.2f}\n"
        f"atr_buy_threshold: {settings.atr_buy_threshold}\n\n"
        "VWAP (Volume Weighted Average Price):\n"
        f"vwap_latest_data: {latest_data['vwap']:.2f}\n"
        f"vwap_previous_data: {previous_data['vwap']:.2f}\n\n"
        "Parabolic SAR:\n"
        f"psar_acceleration: {settings.psar_acceleration}\n"
        f"psar_maximum: {settings.psar_maximum}\n"
        f"psar_latest_data: {latest_data['psar']:.2f}\n"
        f"psar_previous_data: {previous_data['psar']:.2f}\n\n"
        "Moving Averages:\n"
        f"ma_50_latest_data: {latest_data['ma_50']:.2f}\n"
        f"ma_200_latest_data: {latest_data['ma_200']:.2f}\n"
        f"ma_50_previous_data: {previous_data['ma_50']:.2f}\n"
        f"ma_200_previous_data: {previous_data['ma_200']:.2f}\n\n"
        "ADX Trend:\n"
        f"adx_timeperiod: {settings.adx_timeperiod}\n"
        f"adx_strong_trend: {settings.adx_strong_trend}\n"
        f"adx_weak_trend: {settings.adx_weak_trend}\n"
        f"adx_no_trend: {settings.adx_no_trend}\n"
        f"adx_latest_data: {latest_data['adx']:.2f}\n"
        f"adx_previous_data: {previous_data['adx']:.2f}\n\n"
        "-- \n\nFomoSapiensCryptoDipHunter\nhttps://fomo.ropeaccess.pro\n\nStefanCryptoTradingBot\nhttps://stefan.ropeaccess.pro\n\nCodeCave\nhttps://cave.ropeaccess.pro\n"
    )

    return subject, content
