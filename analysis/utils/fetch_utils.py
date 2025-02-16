from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
from binance.client import Client
import os
from fomo_sapiens.utils.exception_handlers import exception_handler

load_dotenv()

def get_binance_api_credentials():
    """
    Retrieves Binance API credentials from environment variables.

    Returns:
        tuple: A tuple containing the API key and API secret.
    """
    api_key = os.environ.get('BINANCE_GENERAL_API_KEY')
    api_secret = os.environ.get('BINANCE_GENERAL_API_SECRET')
    
    return api_key, api_secret


@exception_handler()
def create_binance_client():
    """
    Creates a Binance client instance using the provided API credentials.

    Args:
        bot_id (str, optional): The bot identifier to retrieve specific API credentials.
        testnet (bool, optional): Whether to use the testnet environment. Default is False.

    Returns:
        Client: The Binance client instance.
    
    Raises:
        Exception: If there is an issue creating the client, an exception is logged and an email is sent to the admin.
    """
    api_key, api_secret = get_binance_api_credentials()
    return Client(api_key, api_secret)


@exception_handler()
def fetch_and_save_df(settings):
    """
    Fetches data for a given trading symbol and interval, processes it into JSON format, 
    and saves the data along with the timestamp of the last fetch to the provided settings.

    Args:
        settings (TechnicalAnalysisSettings): The settings object containing the user's symbol, 
                                              interval, and other configuration details.

    This function fetches market data using the `fetch_data` function, converts the resulting 
    DataFrame to JSON format, and stores it in the `df` field of the `settings` model. 
    The timestamp of the fetch is also recorded in the `df_last_fetch_time` field.
    """
    from datetime import datetime as dt 
    df_fetched = fetch_data(symbol=settings.symbol, interval=settings.interval, lookback=calculate_lookback_extended(settings))
    json_data = df_fetched.to_json(orient='records')
    settings.df = json_data
    settings.df_last_fetch_time = dt.now()
    settings.save()


@exception_handler()
def calculate_lookback_extended(settings):
    """
    Calculates the extended lookback period based on the interval set in the provided settings.

    Args:
        settings (TechnicalAnalysisSettings): The settings object containing the interval configuration.

    Returns:
        str: The extended lookback period in the format 'xY', where x is the number of units 
             multiplied by 205 (based on the interval), and Y is the time unit (e.g., 'm', 'h', etc.).

    Example:
        If the interval is '5m', the function returns '1025m' (5 * 205).
    """
    lookback_extended = f'{int(settings.interval[:-1]) * 205}{settings.interval[-1:]}'
    return lookback_extended


@exception_handler()
def fetch_data(symbol, interval='1h', lookback='2d', start_str=None, end_str=None):
    """
    Fetch historical kline (candlestick) data for a specific trading symbol.

    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
        interval (str, optional): The interval between each candlestick. Default is '1m'.
        lookback (str, optional): The lookback period for historical data. Can be in hours (e.g., '4h'), days (e.g., '2d'), or minutes (e.g., '30m'). Default is '4h'.
        start_str (str, optional): The start time for the historical data. If None, it uses the lookback period.
        end_str (str, optional): The end time for the historical data. If None, it uses the current time.

    Returns:
        pd.DataFrame: A DataFrame containing the historical kline data.

    Raises:
        BinanceAPIException: If there is an error from the Binance API.
        ConnectionError: If there is a connection error.
        TimeoutError: If there is a timeout error.
        ValueError: If an invalid lookback period format is provided.
        Exception: For any other exception, an email is sent to the admin.
    """
    general_client = create_binance_client()
    
    klines = None
    
    if not start_str and not end_str:
        if lookback[-1] == 'h':
            hours = int(lookback[:-1])
            start_time = datetime.utcnow() - timedelta(hours=hours)
        elif lookback[-1] == 'd':
            days = int(lookback[:-1])
            start_time = datetime.utcnow() - timedelta(days=days)
        elif lookback[-1] == 'm':
            minutes = int(lookback[:-1])
            start_time = datetime.utcnow() - timedelta(minutes=minutes)
        else:
            raise ValueError("Unsupported lookback period format.")
        
        start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        
        klines = general_client.get_historical_klines(
            symbol=symbol, 
            interval=interval, 
            start_str=start_str
        )
    else:
        klines = general_client.get_historical_klines(
            symbol=symbol, 
            interval=interval, 
            start_str=str(start_str), 
            end_str=str(end_str)
        )
    
    df = pd.DataFrame(
        klines, 
        columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'number_of_trades', 
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 
            'ignore'
        ]
    )
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    
    return df
    

@exception_handler()
def fetch_system_status():
    """
    Fetches the current system status from the Binance API.

    Returns:
        dict: A dictionary containing the system status if the request is successful, otherwise returns None.
    """
    general_client = create_binance_client()
    status = general_client.get_system_status()
    return status


@exception_handler()
def fetch_server_time():
    """
    Fetches the current server time from the Binance API.

    Returns:
        dict: A dictionary containing the server time if the request is successful, otherwise returns None.
    """
    general_client = create_binance_client()
    server_time = general_client.get_server_time()
    return server_time