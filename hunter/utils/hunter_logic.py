from DipHunterCryptoTechnicalAnalysis.utils.logging import logger
from DipHunterCryptoTechnicalAnalysis.utils.exception_handlers import exception_handler
from analysis.utils.calc_utils import calculate_ta_indicators
from analysis.utils.fetch_utils import fetch_data
from hunter.utils.calc_utils import calculate_ta_averages, check_ta_trend
from hunter.utils.sell_signals import check_classic_ta_sell_signal
from hunter.utils.buy_signals import check_classic_ta_buy_signal
from DipHunterCryptoTechnicalAnalysis.utils.email_utils import send_email

@exception_handler()
def run_single_hunter_logic(hunter_settings):
    """
    Runs the trading logic for a single bot based on its settings.

    This function fetches market data, validates it, and executes the trading logic based on 
    the bot's current settings and analysis methods. The trading logic includes checking 
    the bot's suspension status, fetching the current price, and managing the trade.

    Args:
        hunter_settings (BotSettings): The settings for the specific bot to run.

    Returns:
        None
    """

    if not hunter_settings:
        logger.info(f"Bot {hunter_settings.id} HunterSettings not found. Cycle skipped.")
        
        symbol = hunter_settings.symbol
        interval = hunter_settings.interval
        lookback_period = hunter_settings.lookback_period
        lookback_extended = f'{int(hunter_settings.interval[:-1]) * 205}{hunter_settings.interval[-1:]}'
        
        logger.trade(f'Bot {hunter_settings.id} {hunter_settings.strategy} Fetching data for {symbol} with interval {interval} and lookback {lookback_period}')
        df_fetched = fetch_data(
            symbol=symbol, 
            interval=interval, 
            lookback=lookback_extended
            )
        
        if df_fetched is None:
            return
        
        df_calculated = calculate_ta_indicators(
            df_fetched, 
            hunter_settings
            )   
        
        trend = check_ta_trend(
            df_calculated, 
            hunter_settings
            )
        
        averages = calculate_ta_averages(
            df_calculated, 
            hunter_settings
            )
        
        buy_singal = check_classic_ta_buy_signal(
            df_calculated, 
            hunter_settings, 
            trend, 
            averages, 
            )
        
        sell_singal = check_classic_ta_sell_signal(
            df_calculated, 
            hunter_settings, 
            trend, 
            averages, 
            )
        
        if buy_singal: 
            send_email(hunter_settings.user.email, 'subject', 'tresc')
        if sell_singal:
            send_email(hunter_settings.user.email, 'subject', 'tresc')