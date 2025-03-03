from pandas import DataFrame
from typing import Union, Dict, Optional, Tuple
from datetime import datetime as dt
from fomo_sapiens.utils.exception_handlers import exception_handler


@exception_handler()
def generate_hunter_signal_email(
    signal: str, hunter: object, df: DataFrame, trend: str, averages: Dict[str, float]
) -> Union[Tuple[str, str], Optional[int]]:
    """
    Generates an email content for the Hunter signal based on various technical indicators and current market data.

    Args:
        signal (str): The type of signal (e.g., "buy", "sell") for which the email is generated.
        hunter (object): The Hunter object containing various settings and market signal configurations.
        df (DataFrame): The DataFrame containing the historical market data used to compute signals.
        trend (str): The current market trend (e.g., "bullish", "bearish").
        averages (dict): A dictionary containing the average values of various indicators.

    Returns:
        str: A formatted email content with details on the signal and relevant technical indicators.

    The email includes information on the following:
        - Hunter's configuration (symbol, interval, lookback, comment)
        - Signal details (signal type, trend, and relevant indicators)
        - The latest and previous market data for each indicator (e.g., close price, volume)
        - Various technical indicators like RSI, CCI, MFI, MACD, Bollinger Bands, etc.

    This function constructs a detailed report of the signal, the relevant technical indicator values,
    and sends it via email. The content is dynamically generated based on the signal and current market data.
    """
    from hunter.utils.hunter_logic import get_latest_and_previus_data

    now = dt.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    latest_data, previous_data = get_latest_and_previus_data(df)

    subject = f"Hunter {hunter.id} {hunter.symbol} {signal.upper()} signal"

    content = (
        f"FomoSapiensCryptoDipHunter\n"
        f"{signal.upper()} signal\n"
        f"{formatted_now}\n\n"
        f"Hunter {hunter.id} {hunter.symbol}\n"
        f"interval: {hunter.interval}\n"
        f"lookback: {hunter.lookback}\n"
        f"comment: {hunter.comment}\n\n"
        f"Hunter details:\n\n"
        f"open_time: {latest_data['open_time']}\n"
        f"close_time: {latest_data['close_time']}\n\n"
        f"trend: {trend}\n\n"
        f"price_signals: {hunter.price_signals}\n"
        f"avg_close_period: {hunter.avg_close_period}\n"
        f"close_latest_data: {latest_data['close']}\n"
        f"close_previous_data: {previous_data['close']}\n"
        f"avg_close: {averages['avg_close']}\n\n"
        f"vol_signals: {hunter.vol_signals}\n"
        f"avg_volume_period: {hunter.avg_volume_period}\n"
        f"volume_latest_data: {latest_data['volume']}\n"
        f"volume_previous_data: {previous_data['volume']}\n"
        f"avg_volume: {averages['avg_volume']}\n\n"
    )

    if hunter.rsi_signals or hunter.rsi_divergence_signals:
        content += (
            "RSI (Relative Strength Index):\n"
            f"rsi_signals: {hunter.rsi_signals}\n"
            f"rsi_divergence_signals: {hunter.rsi_divergence_signals}\n"
            f"rsi_timeperiod: {hunter.rsi_timeperiod}\n"
            f"avg_rsi_period: {hunter.avg_rsi_period}\n"
            f"rsi_latest_data: {latest_data['rsi']}\n"
            f"rsi_previous_data: {previous_data['rsi']}\n"
            f"avg_rsi: {averages['avg_rsi']}\n"
            f"rsi_buy: {hunter.rsi_buy}\n"
            f"rsi_sell: {hunter.rsi_sell}\n\n"
        )

    if hunter.cci_signals or hunter.cci_divergence_signals:
        content += (
            "CCI (Commodity Channel Index):\n"
            f"cci_signals: {hunter.cci_signals}\n"
            f"cci_divergence_signals: {hunter.cci_divergence_signals}\n"
            f"cci_timeperiod: {hunter.cci_timeperiod}\n"
            f"avg_cci_period: {hunter.avg_cci_period}\n"
            f"cci_latest_data: {latest_data['cci']}\n"
            f"cci_previous_data: {previous_data['cci']}\n"
            f"avg_cci: {averages['avg_cci']}\n"
            f"cci_buy: {hunter.cci_buy}\n"
            f"cci_sell: {hunter.cci_sell}\n\n"
        )

    if hunter.mfi_signals or hunter.mfi_divergence_signals:
        content += (
            "MFI (Money Flow Index):\n"
            f"mfi_signals: {hunter.mfi_signals}\n"
            f"mfi_divergence_signals: {hunter.mfi_divergence_signals}\n"
            f"mfi_timeperiod: {hunter.mfi_timeperiod}\n"
            f"avg_mfi_period: {hunter.avg_mfi_period}\n"
            f"mfi_latest_data: {latest_data['mfi']}\n"
            f"mfi_previous_data: {previous_data['mfi']}\n"
            f"avg_mfi: {averages['avg_mfi']}\n"
            f"mfi_buy: {hunter.mfi_buy}\n"
            f"mfi_sell: {hunter.mfi_sell}\n\n"
        )

    if hunter.macd_cross_signals or hunter.macd_histogram_signals:
        content += (
            "MACD (Moving Average Convergence Divergence):\n"
            f"macd_cross_signals: {hunter.macd_cross_signals}\n"
            f"macd_histogram_signals: {hunter.macd_histogram_signals}\n"
            f"macd_timeperiod: {hunter.macd_timeperiod}\n"
            f"macd_signalperiod: {hunter.macd_signalperiod}\n"
            f"avg_macd_period: {hunter.avg_macd_period}\n"
            f"macd_latest_data: {latest_data['macd']}\n"
            f"macd_signal_latest_data: {latest_data['macd_signal']}\n"
            f"macd_previous_data: {previous_data['macd']}\n"
            f"macd_signal_previous_data: {previous_data['macd_signal']}\n"
            f"avg_macd: {averages['avg_macd']}\n"
            f"avg_macd_signal: {averages['avg_macd_signal']}\n\n"
        )

    if hunter.bollinger_signals:
        content += (
            "Bollinger Bands:\n"
            f"bollinger_signals: {hunter.bollinger_signals}\n"
            f"bollinger_timeperiod: {hunter.bollinger_timeperiod}\n"
            f"bollinger_nbdev: {hunter.bollinger_nbdev}\n"
            f"upper_band_latest_data: {latest_data['upper_band']}\n"
            f"middle_band_latest_data: {latest_data['middle_band']}\n"
            f"lower_band_latest_data: {latest_data['lower_band']}\n"
            f"upper_band_previous_data: {previous_data['upper_band']}\n"
            f"middle_band_previous_data: {previous_data['middle_band']}\n"
            f"lower_band_previous_data: {previous_data['lower_band']}\n\n"
        )

    if hunter.stoch_signals or hunter.stoch_divergence_signals:
        content += (
            "Stochastic Indicators:\n"
            f"stoch_signals: {hunter.stoch_signals}\n"
            f"stoch_divergence_signals: {hunter.stoch_divergence_signals}\n"
            f"stoch_k_timeperiod: {hunter.stoch_k_timeperiod}\n"
            f"stoch_d_timeperiod: {hunter.stoch_d_timeperiod}\n"
            f"avg_stoch_period: {hunter.avg_stoch_period}\n"
            f"stoch_k_latest_data: {latest_data['stoch_k']}\n"
            f"stoch_d_latest_data: {latest_data['stoch_d']}\n"
            f"stoch_k_previous_data: {previous_data['stoch_k']}\n"
            f"stoch_d_previous_data: {previous_data['stoch_d']}\n"
            f"avg_stoch_k: {averages['avg_stoch_k']}\n"
            f"avg_stoch_d: {averages['avg_stoch_d']}\n"
            f"stoch_buy: {hunter.stoch_buy}\n"
            f"stoch_sell: {hunter.stoch_sell}\n\n"
        )

    if hunter.stoch_rsi_signals:
        content += (
            "Stochastic RSI Indicators:\n"
            f"stoch_rsi_signals: {hunter.stoch_rsi_signals}\n"
            f"stoch_rsi_timeperiod: {hunter.stoch_rsi_timeperiod}\n"
            f"stoch_rsi_k_timeperiod: {hunter.stoch_rsi_k_timeperiod}\n"
            f"stoch_rsi_d_timeperiod: {hunter.stoch_rsi_d_timeperiod}\n"
            f"avg_stoch_rsi_period: {hunter.avg_stoch_rsi_period}\n"
            f"stoch_rsi_d_latest_data: {latest_data['stoch_rsi_d']}\n"
            f"stoch_rsi_k_latest_data: {latest_data['stoch_rsi_k']}\n"
            f"stoch_rsi_d_previous_data: {previous_data['stoch_rsi_d']}\n"
            f"stoch_rsi_k_previous_data: {previous_data['stoch_rsi_k']}\n"
            f"avg_stoch_rsi_d: {averages['avg_stoch_rsi_d']}\n"
            f"avg_stoch_rsi_k: {averages['avg_stoch_rsi_k']}\n\n"
        )

    if hunter.ema_cross_signals or hunter.ema_fast_signals or hunter.ema_slow_signals:
        content += (
            "EMA (Exponential Moving Averages):\n"
            f"ema_cross_signals: {hunter.ema_cross_signals}\n"
            f"ema_fast_signals: {hunter.ema_fast_signals}\n"
            f"ema_slow_signals: {hunter.ema_slow_signals}\n"
            f"ema_fast_timeperiod: {hunter.ema_fast_timeperiod}\n"
            f"ema_slow_timeperiod: {hunter.ema_slow_timeperiod}\n"
            f"avg_ema_period: {hunter.avg_ema_period}\n"
            f"ema_fast_latest_data: {latest_data['ema_fast']}\n"
            f"ema_slow_latest_data: {latest_data['ema_slow']}\n"
            f"ema_fast_previous_data: {previous_data['ema_fast']}\n"
            f"ema_slow_previous_data: {previous_data['ema_slow']}\n"
            f"avg_ema_fast: {averages['avg_ema_fast']}\n"
            f"avg_ema_slow: {averages['avg_ema_slow']}\n\n"
        )

    if hunter.di_signals:
        content += (
            "Directional Movement Index (DMI):\n"
            f"di_signals: {hunter.di_signals}\n"
            f"di_timeperiod: {hunter.di_timeperiod}\n"
            f"avg_di_period: {hunter.avg_di_period}\n"
            f"plus_di_latest_data: {latest_data['plus_di']}\n"
            f"minus_di_latest_data: {latest_data['minus_di']}\n"
            f"plus_di_previous_data: {previous_data['plus_di']}\n"
            f"minus_di_previous_data: {previous_data['minus_di']}\n"
            f"avg_plus_di: {averages['avg_plus_di']}\n"
            f"avg_minus_di: {averages['avg_minus_di']}\n\n"
        )

    if hunter.atr_signals:
        content += (
            "ATR (Average True Range):\n"
            f"atr_signals: {hunter.atr_signals}\n"
            f"atr_timeperiod: {hunter.atr_timeperiod}\n"
            f"avg_atr_period: {hunter.avg_atr_period}\n"
            f"atr_latest_data: {latest_data['atr']}\n"
            f"atr_previous_data: {previous_data['atr']}\n"
            f"avg_atr: {averages['avg_atr']}\n"
            f"atr_buy_threshold: {hunter.atr_buy_threshold}\n\n"
        )

    if hunter.vwap_signals:
        content += (
            "VWAP (Volume Weighted Average Price):\n"
            f"vwap_signals: {hunter.vwap_signals}\n"
            f"avg_vwap_period: {hunter.avg_vwap_period}\n"
            f"vwap_latest_data: {latest_data['vwap']}\n"
            f"vwap_previous_data: {previous_data['vwap']}\n"
            f"avg_vwap: {averages['avg_vwap']}\n\n"
        )

    if hunter.psar_signals:
        content += (
            "Parabolic SAR:\n"
            f"psar_signals: {hunter.psar_signals}\n"
            f"psar_acceleration: {hunter.psar_acceleration}\n"
            f"psar_maximum: {hunter.psar_maximum}\n"
            f"avg_psar_period: {hunter.avg_psar_period}\n"
            f"psar_latest_data: {latest_data['psar']}\n"
            f"psar_previous_data: {previous_data['psar']}\n"
            f"avg_psar: {averages['avg_psar']}\n\n"
        )

    if hunter.ma50_signals or hunter.ma200_signals or hunter.ma_cross_signals:
        content += (
            "Moving Averages:\n"
            f"ma50_signals: {hunter.ma50_signals}\n"
            f"ma200_signals: {hunter.ma200_signals}\n"
            f"ma_cross_signals: {hunter.ma_cross_signals}\n"
            f"ma_50_latest_data: {latest_data['ma_50']}\n"
            f"ma_200_latest_data: {latest_data['ma_200']}\n"
            f"ma_50_previous_data: {previous_data['ma_50']}\n"
            f"ma_200_previous_data: {previous_data['ma_200']}\n\n"
        )

    if hunter.trend_signals:
        content += (
            "ADX Trend:\n"
            f"trend_signals: {hunter.trend_signals}\n"
            f"adx_timeperiod: {hunter.adx_timeperiod}\n"
            f"avg_adx_period: {hunter.avg_adx_period}\n"
            f"adx_strong_trend: {hunter.adx_strong_trend}\n"
            f"adx_weak_trend: {hunter.adx_weak_trend}\n"
            f"adx_no_trend: {hunter.adx_no_trend}\n"
            f"adx_latest_data: {latest_data['adx']}\n"
            f"adx_previous_data: {previous_data['adx']}\n"
            f"avg_adx: {averages['avg_adx']}\n\n"
        )

    content += "-- \n\nFomoSapiensCryptoDipHunter\nhttps://fomo.ropeaccess.pro\n\nStefanCryptoTradingBot\nhttps://stefan.ropeaccess.pro\n\nCodeCave\nhttps://cave.ropeaccess.pro\n"
    
    return subject, content
