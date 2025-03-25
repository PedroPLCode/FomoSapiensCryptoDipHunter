import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from analysis.models import SentimentAnalysis
from fomo_sapiens.utils.logging import logger
from fomo_sapiens.utils.exception_handlers import exception_handler
from fomo_sapiens.utils.retry_connection import retry_connection

nltk.download("vader_lexicon")


@exception_handler()
@retry_connection()
def get_crypto_news_rss(url: str) -> List[str]:
    """
    Fetches the latest cryptocurrency news from an RSS feed.

    This function sends a request to the given RSS feed URL, parses the XML response,
    extracts the first 30 news items, and combines their titles and descriptions.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        List[str]: A list of strings, each containing the title and description of a news item.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "xml")

    news_items: List[str] = []
    for item in soup.find_all("item")[:30]:
        title: str = item.title.text
        description: str = item.description.text
        news_items.append(f"{title} {description}")

    return news_items


@exception_handler()
def analyze_sentiment(text: str) -> Tuple[float, str]:
    """
    Analyzes the sentiment of a given text using the VADER sentiment analysis tool.

    This function calculates the sentiment score of the input text and classifies it
    as "Positive", "Negative", or "Neutral" based on the compound score.

    Args:
        text (str): The text to be analyzed.

    Returns:
        Tuple[float, str]: A tuple containing the sentiment score (float) and its label (str).
                           - Score > 0.05 → "Positive"
                           - Score < -0.05 → "Negative"
                           - Otherwise → "Neutral"
    """
    sia = SentimentIntensityAnalyzer()
    score: float = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        label: str = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return score, label


@exception_handler()
def fetch_and_save_sentiment_analysis() -> None:
    """
    Fetches cryptocurrency news from multiple sources, analyzes their sentiment,
    and updates or creates a single database entry with the latest sentiment analysis.

    This function retrieves news articles from Cointelegraph and Coindesk,
    calculates their sentiment scores, and updates the database entry with ID=1
    to store the most recent sentiment data.

    Returns:
        None
    """
    cointelegraph_news = get_crypto_news_rss("https://cointelegraph.com/rss")[:25]
    coindesk_news = get_crypto_news_rss(
        "https://www.coindesk.com/arc/outboundfeeds/rss/"
    )[:25]
    all_news = cointelegraph_news + coindesk_news

    if not all_news:
        logger.warning("No news articles found for sentiment analysis.")
        return

    total_sentiment_score = 0
    for news_text in all_news:
        sentiment_score, _ = analyze_sentiment(news_text)
        total_sentiment_score += sentiment_score

    avg_sentiment_score = total_sentiment_score / len(all_news)

    if avg_sentiment_score >= 0.05:
        avg_sentiment_label = "Positive"
    elif avg_sentiment_score <= -0.05:
        avg_sentiment_label = "Negative"
    else:
        avg_sentiment_label = "Neutral"

    SentimentAnalysis.objects.update_or_create(
        id=1,
        defaults={
            "sentiment_score": avg_sentiment_score,
            "sentiment_label": avg_sentiment_label,
        },
    )

    logger.info(f"Sentiment updated: {avg_sentiment_label} ({avg_sentiment_score})")
