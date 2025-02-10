from datetime import datetime as dt
from fomo_sapiens.utils.logging import logger
from fomo_sapiens.utils.exception_handlers import exception_handler
from analysis.utils.calc_utils import calculate_ta_indicators, calculate_ta_averages, check_ta_trend
from analysis.utils.fetch_utils import fetch_data, calculate_lookback_extended
from hunter.utils.sell_signals import check_classic_ta_sell_signal
from hunter.utils.buy_signals import check_classic_ta_buy_signal
from report_utils import generate_hunter_signal_email
from hunter.models import TechnicalAnalysisHunter
from fomo_sapiens.utils.email_utils import send_email
from analysis.utils.calc_utils import is_df_valid

@exception_handler()
def run_selected_interval_hunters(interval):
    all_selected_hunters = TechnicalAnalysisHunter.query.filter_by(interval=interval).all()
    
    if not all_selected_hunters:
        return
    
    for hunter in all_selected_hunters:
        try:
            run_single_hunter_logic(hunter)
        except Exception as e:
            logger.error(f"Error running hunter {hunter.id}: {e}")


@exception_handler()
def run_single_hunter_logic(hunter):
    """
    Runs the trading logic for a single bot based on its settings.

    This function fetches market data, validates it, and executes the trading logic based on 
    the bot's current settings and analysis methods. The trading logic includes checking 
    the bot's suspension status, fetching the current price, and managing the trade.

    Args:
        hunter (BotSettings): The settings for the specific bot to run.

    Returns:
        None
    """

    if not hunter:
        logger.info(f"Bot {hunter.id} HunterSettings not found. Cycle skipped.")
        
        symbol = hunter.symbol
        interval = hunter.interval
        signal = 'no'
        
        df_fetched = fetch_data(
            symbol=symbol, 
            interval=interval, 
            lookback=calculate_lookback_extended(hunter)
            )
        
        if not is_df_valid(df_fetched):
            return
        
        df_calculated = calculate_ta_indicators(
            df_fetched, 
            hunter
            )   
        
        trend = check_ta_trend(
            df_calculated, 
            hunter
            )
        
        averages = calculate_ta_averages(
            df_calculated, 
            hunter
            )
        
        buy_singal = check_classic_ta_buy_signal(
            df_calculated, 
            hunter, 
            trend, 
            averages, 
            )
        
        sell_singal = check_classic_ta_sell_signal(
            df_calculated, 
            hunter, 
            trend, 
            averages, 
            )
        
        if buy_singal or sell_singal: 
            signal = 'buy' if buy_singal else 'sell'
            email = hunter.user.email
            subject, content = generate_hunter_signal_email(signal, hunter, df_calculated, trend, averages)
            send_email(email, subject, content)
            
        logger.info(f'Hunter {hunter.id} {hunter.symbol} {hunter.interval} {hunter.period} {hunter.comment} {signal.upper()} signal.')
            

@exception_handler(default_return=(None, None))
def get_latest_and_previus_data(df):
    latest_data = df.iloc[-1]
    previous_data = df.iloc[-2]
    return latest_data, previous_data