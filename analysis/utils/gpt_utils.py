import os
import json
import time
import pandas as pd
from io import StringIO
from openai import OpenAI
from django.utils import timezone
from dotenv import load_dotenv
from typing import Dict, Any
from ..models import TechnicalAnalysisSettings, SentimentAnalysis
from fomo_sapiens.utils.logging import logger
from ..utils.fetch_utils import fetch_and_save_df
from analysis.utils.calc_utils import calculate_ta_indicators
from fomo_sapiens.utils.exception_handlers import exception_handler
from fomo_sapiens.utils.retry_connection import retry_connection
from .msg_utils import generate_gpt_analyse_msg_content
from fomo_sapiens.utils.email_utils import send_email
from fomo_sapiens.utils.telegram_utils import send_telegram

load_dotenv()


@exception_handler()
def format_openai_error(e: Exception) -> Dict[str, Any]:
    """
    Converts any OpenAI-related exception into a clean JSON-ready structure.
    The function is 100% safe: no KeyErrors, no missing attributes.
    """
    http_status = getattr(e, "http_status", "N/A")
    error_code = getattr(e, "code", "N/A")
    error_type = getattr(e, "type", e.__class__.__name__)
    error_message = str(e)

    analysis_message = (
        "Analysis Not Available: OpenAI Response Error occured. "
        f"error_type: {error_type}, "
        f"http_status: {http_status}, "
        f"error_code: {error_code}, "
        f"error_message: {error_message}."
    )

    return {
        "model": "N/A",
        "timestamp": timezone.now().isoformat(),
        "symbol": "N/A",
        "interval": "N/A",
        "analysis": analysis_message,
    }
    

@exception_handler()
@retry_connection()
def fetch_save_and_send_gpt_analysis(username: str | None = None) -> None:
    """
    Fetches the latest cryptocurrency data and news for a specific user or all users, calculates technical indicators,
    sends the data to the GPT model for analysis, and stores the GPT response in the database.

    The function performs the following steps for each user with TechnicalAnalysisSettings:
    1. Fetches and updates the user's cryptocurrency price data.
    2. Converts the stored DataFrame JSON to a Pandas DataFrame and calculates technical indicators.
    3. Retrieves the latest crypto news headlines from the SentimentAnalysis model.
    4. Constructs a prompt including the user's GPT prompt, recent crypto news, and calculated indicators.
    5. Sends the prompt to OpenAI GPT via the API and parses the JSON response.
    6. Saves the GPT response and the timestamp in the user's TechnicalAnalysisSettings.
    7. Optionally sends the analysis via Telegram or email if the user has enabled notifications.

    Raises:
        Any exceptions related to database operations or API calls are handled by the
        `@exception_handler` and `@retry_connection` decorators.
    """
    sentiment_analysis: SentimentAnalysis | None = SentimentAnalysis.objects.filter(id=1).first()
    if not sentiment_analysis.use_gpt_analysis:
        return

    selected_users_ta_settings = TechnicalAnalysisSettings.objects.filter(
        use_gpt_analysis=True, 
        gpt_model__isnull=False, 
        gpt_prompt__isnull=False
    )
    
    if username:
        selected_users_ta_settings = selected_users_ta_settings.filter(user__username=username)

    crypto_news = (
        getattr(sentiment_analysis, "sentiment_news_content", [])
        if sentiment_analysis
        else "Not available"
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key, timeout=900)

    for user_ta_settings in selected_users_ta_settings:
        fetch_and_save_df(user_ta_settings)
        df_loaded: pd.DataFrame = pd.read_json(StringIO(user_ta_settings.df))
        df_calculated: pd.DataFrame = calculate_ta_indicators(df_loaded, user_ta_settings)
        gpt_prompt: str = getattr(user_ta_settings, "gpt_prompt", "")
        gpt_model: str = getattr(user_ta_settings, "gpt_model", "gpt-4o-mini")

        content = (
            f"{gpt_prompt}\n\n"
            f"Symbol to analyse:\n{user_ta_settings.symbol}\n\n"
            f"Interval to analyse:\n{user_ta_settings.interval}\n\n"
            f"Recent crypto news headlines:\n{crypto_news}\n\n"
            f"Technical indicators data calculated with timeperiod {user_ta_settings.general_timeperiod}:\n{df_calculated}"
        )

        response_json = None

        for i in range(3):
            try:
                response = client.chat.completions.create(
                    model=gpt_model,
                    messages=[{"role": "user", "content": content}],
                    response_format={"type": "json_object"}
                )
                response_json = json.loads(response.choices[0].message["content"])
                break

            except Exception as e:
                logger.warning(f"Attempt {i+1}: GPT request failed for user {user_ta_settings.user.username}: {e}")
                if i < 2:
                    time.sleep(3)
                else:
                    response_json = format_openai_error(e)

        user_ta_settings.gpt_response = response_json
        user_ta_settings.gpt_last_update_time = timezone.now()
        user_ta_settings.save()

        msg_subject, msg_content = generate_gpt_analyse_msg_content(response_json)
        if user_ta_settings.user.telegram_gpt_analysis_receiver and user_ta_settings.user.telegram_chat_id:
            send_telegram(chat_id=user_ta_settings.user.telegram_chat_id, msg=msg_content)
        if user_ta_settings.user.email_gpt_analysis_receiver and user_ta_settings.user.email:
            msg_content += (
                f"\n\n-- \n\n"
                "FomoSapiensCryptoDipHunter\nhttps://fomo.ropeaccess.pro\n\n"
                "StefanCryptoTradingBot\nhttps://stefan.ropeaccess.pro\n\n"
                "CodeCave\nhttps://cave.ropeaccess.pro\n"
            )
            send_email(user_ta_settings.user.email, msg_subject, msg_content)

        time.sleep(3)
