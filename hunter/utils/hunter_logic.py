from fomo_sapiens.utils.logging import logger
from django.apps import apps
import time
from typing import Tuple, Any
from fomo_sapiens.utils.exception_handlers import exception_handler
from hunter.utils.sell_signals import check_classic_ta_sell_signal
from hunter.utils.buy_signals import check_classic_ta_buy_signal
from hunter.utils.report_utils import generate_hunter_signal_email
from fomo_sapiens.utils.email_utils import send_email
from fomo_sapiens.utils.telegram_utils import send_telegram
from analysis.utils.calc_utils import is_df_valid
from analysis.utils.calc_utils import (
    calculate_ta_indicators,
    calculate_ta_averages,
    check_ta_trend,
)
from analysis.utils.fetch_utils import (
    fetch_data,
    calculate_lookback_extended,
    fetch_and_save_df,
)


@exception_handler()
def run_selected_interval_hunters(interval: str = "1h") -> None:
    """
    Runs the trading logic for all selected hunters at a given interval.

    This function iterates through all the hunters configured with the specified
    interval and runs their logic. If no hunters are found for the given interval,
    the function will log a message and return without executing any logic.

    Args:
        interval (str): The time interval for the hunter, default is '1h'.
                         Valid intervals can include '1h', '15m', '30m', etc.

    Returns:
        None
    """
    apps.check_apps_ready()
    logger.info(f"Start run_selected_interval_hunters interval {interval}")

    time.sleep(2)

    from hunter.models import TechnicalAnalysisHunter

    all_selected_hunters = TechnicalAnalysisHunter.objects.filter(interval=interval)
    last_hunter = all_selected_hunters.last()
    last_hunter_id = last_hunter.id if last_hunter else 1


    if not all_selected_hunters:
        logger.info(
            f"run_selected_interval_hunters interval {interval}. not all_selected_hunters"
        )
        return

    for hunter in all_selected_hunters:
        try:
            run_single_hunter_logic(hunter, last_hunter_id)
        except Exception as e:
            logger.error(f"Error running hunter {hunter.id}: {e}")
            continue

    logger.info(f"run_selected_interval_hunters interval {interval} completed")


@exception_handler()
def run_single_hunter_logic(hunter: object, last_hunter_id: int) -> None:
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
        return

    symbol = hunter.symbol
    interval = hunter.interval
    signal = None

    df_fetched = fetch_data(
        symbol=symbol, interval=interval, lookback=calculate_lookback_extended(hunter)
    )

    if not is_df_valid(df_fetched):
        return

    df_calculated = calculate_ta_indicators(df_fetched, hunter)

    trend = check_ta_trend(df_calculated, hunter)

    averages = calculate_ta_averages(df_calculated, hunter)

    if hunter.running:

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
            signal = "buy" if buy_singal else "sell"
            subject, content = generate_hunter_signal_email(
                signal, hunter, df_calculated, trend, averages
            )
            if hunter.user.email_signals_receiver and hunter.user.email:
                send_email(hunter.user.email, subject, content)
            if hunter.user.telegram_signals_receiver and hunter.user.telegram_chat_id:
                send_telegram(chat_id=hunter.user.telegram_chat_id, msg=content)

        logger.info(
            f'Hunter {hunter.id} {hunter.symbol} {hunter.interval} {hunter.lookback} {hunter.comment} {signal.upper() if signal else "NO"} signal.'
        )

    else:
        logger.info(
            f"Hunter {hunter.id} {hunter.symbol} {hunter.interval} {hunter.lookback} {hunter.comment} is sleeping."
        )

    fetch_and_save_df(hunter)
    logger.info(
        f"Hunter {hunter.id} {hunter.symbol} {hunter.interval} {hunter.lookback} {hunter.comment} df fetched and saved in db."
    )

    if hunter.id == last_hunter_id:
        user_ta_settings = hunter.user.technicalanalysissettings
        fetch_and_save_df(user_ta_settings)
        logger.info(
            f"User {hunter.user.username} df {user_ta_settings.symbol} {user_ta_settings.interval} {user_ta_settings.lookback} fetched and saved in db."
        )


@exception_handler(default_return=(None, None))
def get_latest_and_previus_data(df: Any) -> Tuple[Any, Any]:
    """
    Fetches the latest and previous data points from the given DataFrame.

    This function extracts the most recent row and the second most recent row from
    the DataFrame, which can then be used for comparison or trend analysis.

    Args:
        df (DataFrame): The DataFrame containing market data.

    Returns:
        tuple: A tuple containing two rows, the latest data and the previous data.
    """
    latest_data = df.iloc[-1]
    previous_data = df.iloc[-2]
    return latest_data, previous_data
