from typing import Union, Tuple
from datetime import datetime as dt
from fomo_sapiens.utils.exception_handlers import exception_handler


@exception_handler()
def generate_gpt_analyse_msg_content(response_json: dict) -> Union[Tuple[str, str], None]:
    """
    Generates the subject and body content for an email or message
    based on the GPT analysis JSON response.

    Args:
        response_json (dict): The JSON response from GPT containing
            keys like 'timestamp', 'model', 'symbol', 'interval', 'analyse'.

    Returns:
        Tuple[str, str]: A tuple containing the email/message subject and content.
        None: If the response_json is empty or invalid.
    """
    now: dt = dt.now()
    formatted_now: str = now.strftime("%Y-%m-%d %H:%M:%S")
    subject: str = "Daily AI-GPT Market Analysis"
    
    if not response_json:
        return subject, "N/A"

    content: str = (
        f"FomoSapiensCryptoDipHunter\n"
        f"https://fomo.ropeaccess.pro\n\n"
        f"Daily AI-GPT Market Analysis.\n"
        f"{formatted_now}\n\n"
        f"Model: {response_json.get('model', 'N/A')}\n"
        f"Timestamp: {response_json.get('timestamp', 'N/A')}\n"
        f"Symbol: {response_json.get('symbol', 'N/A')}\n"
        f"Interval: {response_json.get('interval', 'N/A')}\n\n"
        f"Situation: {response_json.get('situation', 'N/A')}\n\n"
        f"Analysis: {response_json.get('analysis', 'N/A')}\n\n"
        f"Recommendation: {response_json.get('recommendation', 'N/A')}"
    )

    return subject, content
