import os
import json
import pandas as pd
from io import StringIO
from openai import OpenAI
from django.utils import timezone
from dotenv import load_dotenv
from typing import Dict, Any
from ..models import TechnicalAnalysisSettings, SentimentAnalysis
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
        "N/A<br>Exception: OpenAI Response Error"
        f"<br>type: {error_type}"
        f"<br>http_status: {http_status}"
        f"<br>code: {error_code}"
        f"<br>message: {error_message}"
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
def get_and_save_gpt_analysis() -> None:
    """
    Fetches the latest cryptocurrency data and news for all users, calculates technical indicators,
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
    all_users_ta_settings = TechnicalAnalysisSettings.objects.all()
    sentiment_analysis: SentimentAnalysis | None = SentimentAnalysis.objects.filter(id=1).first()
    crypto_news = (
        getattr(sentiment_analysis, "sentiment_news_content", [])
        if sentiment_analysis
        else "Not available"
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    for user_ta_settings in all_users_ta_settings:
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

        try:
            response: Any = client.chat.completions.create(
                model=gpt_model,
                messages=[{"role": "user", "content": content}],
            )

            choice = response.choices[0]
            content_text: str | None = getattr(choice.message, "content", None)
            response_extracted: str = content_text.strip() if content_text else "{}"
            
            try:
                response_json: dict = json.loads(response_extracted)
            except json.JSONDecodeError:
                response_json = {
                    "model": gpt_model,
                    "timestamp": timezone.now().isoformat(),
                    "symbol": "N/A",
                    "interval": "N/A",
                    "analysis": "json.JSONDecodeError: Invalid JSON returned from GPT model."
                }
                
            user_ta_settings.gpt_response = response_json

        except Exception as e:
            user_ta_settings.gpt_response = format_openai_error(e)

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
