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


@exception_handler(default_return=[])
@retry_connection()
def get_crypto_news_rss(url: str, news_amount: int) -> List[str]:
    """
    Fetches the latest cryptocurrency news from an RSS feed.

    Args:
        url (str): The URL of the RSS feed.
        news_amount (int): The number of news articles to fetch.

    Returns:
        List[str]: A list of news titles and descriptions.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "xml")

    news_items: List[str] = []
    for item in soup.find_all("item")[:news_amount]:
        title: str = item.title.text
        description: str = item.description.text
        news_items.append(f"{title} {description}")

    return news_items


@exception_handler(default_return=(0, "Unknown"))
def analyze_sentiment(text: str) -> Tuple[float, str]:
    """
    Analyzes the sentiment of a text using VADER.

    Args:
        text (str): The text to analyze.

    Returns:
        Tuple[float, str]: The sentiment score and label ("Positive", "Negative", "Neutral").
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
    Fetches cryptocurrency news from various sources, analyzes their sentiment, and updates the database.

    Returns:
        None
    """
    sentiment_analysis = SentimentAnalysis.objects.filter(id=1).first()
    if not sentiment_analysis:
        sentiment_analysis = SentimentAnalysis.objects.create()

    all_news = []
    news_urls = sentiment_analysis.sentiment_news_sources
    news_amount = sentiment_analysis.sentiment_news_amount
    
    for url in news_urls:
        news = get_crypto_news_rss(url, news_amount)
        all_news.extend(news[:sentiment_analysis.sentiment_news_amount])

    if not all_news:
        logger.warning("No news articles found for sentiment analysis.")
        return

    total_sentiment_score = sum(
        analyze_sentiment(news_text)[0] for news_text in all_news
    )
    avg_sentiment_score = total_sentiment_score / len(all_news)

    avg_sentiment_label = (
        "Positive"
        if avg_sentiment_score >= 0.05
        else "Negative" if avg_sentiment_score <= -0.05 else "Neutral"
    )

    SentimentAnalysis.objects.update_or_create(
        pk=1,
        defaults={
            "sentiment_score": avg_sentiment_score,
            "sentiment_label": avg_sentiment_label,
        },
    )

    logger.info(f"Sentiment updated: {avg_sentiment_label} ({avg_sentiment_score})")
