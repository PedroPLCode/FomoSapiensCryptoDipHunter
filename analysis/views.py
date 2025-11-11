from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from io import StringIO
import pandas as pd
from .forms import TechnicalAnalysisSettingsForm
from .models import TechnicalAnalysisSettings, SentimentAnalysis
from fomo_sapiens.models import UserProfile
from fomo_sapiens.utils.exception_handlers import exception_handler
from fomo_sapiens.utils.email_utils import send_email
from .utils.fetch_utils import fetch_and_save_df
from analysis.utils.calc_utils import calculate_ta_indicators
from analysis.utils.report_utils import generate_ta_report_email
from analysis.utils.msg_utils import generate_gpt_analyse_msg_content
from analysis.utils.sentiment_utils import fetch_and_save_sentiment_analysis
from analysis.utils.gpt_utils import get_and_save_gpt_analysis
from .utils.plot_utils import (
    plot_selected_ta_indicators,
    prepare_selected_indicators_list,
)


@exception_handler(default_return=lambda: redirect("show_technical_analysis"))
@login_required
def update_technical_analysis_settings(request: HttpRequest) -> HttpResponse:
    """
    View function to update the user's technical analysis settings.

    This function handles both displaying the settings form and processing the submitted form.
    If the request method is POST, it validates and saves the form data. If successful, the
    settings are updated, and new technical analysis data is fetched and saved.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the settings page or redirects upon successful update.
    """
    user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = TechnicalAnalysisSettingsForm(request.POST, instance=user_ta_settings)
        if form.is_valid():
            form.save()
            fetch_and_save_df(user_ta_settings)
            messages.success(request, "Settings saved succesfully.")
            return redirect("show_technical_analysis")
    else:
        form = TechnicalAnalysisSettingsForm(instance=user_ta_settings)

    return render(request, "analysis/change_settings.html", {"form": form})


@exception_handler(default_return=lambda: redirect("show_technical_analysis"))
@login_required
def refresh_technical_analysis(request: HttpRequest) -> HttpResponse:
    """
    View function to refresh the user's technical analysis data.

    This function retrieves or creates the user's technical analysis settings,
    updates the analysis data, and informs the user upon successful completion.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the technical analysis page after refreshing the data.
    """
    user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
        user=request.user
    )
    fetch_and_save_df(user_ta_settings)
    messages.success(request, "Technical Analysis refreshed successfully")
    return redirect("show_technical_analysis")


@exception_handler(default_return=lambda: redirect("show_technical_analysis"))
def refresh_sentiment_analysis(request: HttpRequest) -> HttpResponse:
    """
    Refreshes the market sentiment analysis data.

    This view triggers the sentiment analysis update by fetching new 
    cryptocurrency news, analyzing their sentiment, and updating the database. 
    After the process is completed, the user is redirected to the 
    technical analysis page with a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the technical analysis page after refreshing the sentiment data.
    """
    fetch_and_save_sentiment_analysis()
    messages.success(request, "Sentiment Analysis refreshed successfully.")
    return redirect("show_technical_analysis")


@exception_handler(default_return=lambda: redirect("show_technical_analysis"))
def show_technical_analysis(request: HttpRequest) -> HttpResponse:
    """
    View function to display technical analysis data.

    This view is accessible to both authenticated users and guests. If a user is authenticated,
    their saved settings are loaded or created. If a guest accesses the page, a guest account
    is used to generate technical analysis data. Users can select technical indicators to be
    displayed, and the latest data is fetched and plotted accordingly.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the technical analysis page with the relevant data and charts.
    """
    if request.user.is_authenticated:
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
            user=request.user
        )
    else:
        guest_user, created = UserProfile.objects.get_or_create(username="guest")
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
            user=guest_user
        )
        fetch_and_save_df(user_ta_settings)

    if request.method == "POST":
        selected_indicators = request.POST.getlist("indicators")
        user_ta_settings.selected_plot_indicators = ",".join(selected_indicators)
        user_ta_settings.save()

    df_loaded = pd.read_json(StringIO(user_ta_settings.df))
    if df_loaded is None or df_loaded.empty:
        messages.success(request, "Error loading data.")
        return render(request, "analysis/show_analysis.html")

    df_calculated = calculate_ta_indicators(df_loaded, user_ta_settings)
    if df_calculated is None or df_calculated.empty:
        messages.success(request, "Error calculating Technical Analysis.")
        return render(request, "analysis/show_analysis.html")

    latest_data = df_calculated.iloc[-1].to_dict()
    previous_data = df_calculated.iloc[-2].to_dict()

    selected_indicators_list = prepare_selected_indicators_list(
        user_ta_settings.selected_plot_indicators
    )
    plot_url = plot_selected_ta_indicators(df_calculated, user_ta_settings)
    indicators_list = [
        "close",
        "rsi",
        "cci",
        "mfi",
        "macd",
        "ema",
        "boll",
        "stoch",
        "stoch_rsi",
        "ma50",
        "ma200",
        "adx",
        "atr",
        "psar",
        "vwap",
        "di",
    ]

    sentiment_analysis = SentimentAnalysis.objects.filter(id=1).first()
    if not sentiment_analysis:
        fetch_and_save_sentiment_analysis()
        sentiment_analysis = SentimentAnalysis.objects.filter(id=1).first()
        
    gpt_analysis = user_ta_settings.gpt_response
    if not gpt_analysis:
        fetch_and_save_sentiment_analysis()
        get_and_save_gpt_analysis()
        if request.user.is_authenticated:
            user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
                user=request.user
            )
        else:
            guest_user, created = UserProfile.objects.get_or_create(username="guest")
            user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
                user=guest_user
            )
        gpt_analysis = user_ta_settings.gpt_response

    return render(
        request,
        "analysis/show_analysis.html",
        {
            "user_ta_settings": user_ta_settings,
            "latest_data": latest_data,
            "previous_data": previous_data,
            "plot_url": plot_url,
            "selected_indicators_list": selected_indicators_list,
            "indicators_list": indicators_list,
            "sentiment_analysis": sentiment_analysis,
            "gpt_analysis": gpt_analysis
        },
    )


@exception_handler(default_return=lambda: redirect("show_technical_analysis"))
@login_required
def send_email_analysis_report(request: HttpRequest) -> HttpResponse:
    """
    Sends a technical analysis report via email to the user.

    This view function retrieves the user's technical analysis settings,
    loads the saved data, calculates indicators, trends, and averages,
    and then generates and sends an email report.

    If data is unavailable or calculations fail, an error message is displayed.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the technical analysis page or displays an error message.
    """
    user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(
        user=request.user
    )

    df_loaded = pd.read_json(StringIO(user_ta_settings.df))
    if df_loaded is None or df_loaded.empty:
        messages.success(request, "Error loading data.")
        return render(request, "analysis/show_analysis.html")

    df_calculated = calculate_ta_indicators(df_loaded, user_ta_settings)
    if df_calculated is None or df_calculated.empty:
        messages.success(request, "Error calculating Technical Analysis.")
        return render(request, "analysis/show_analysis.html")

    if user_ta_settings.user.email:
        email = user_ta_settings.user.email
        ai_response = user_ta_settings.gpt_response
        ta_subject, ta_content = generate_ta_report_email(user_ta_settings, df_calculated)
        ai_subject, ai_content = generate_gpt_analyse_msg_content(ai_response)
        ai_content += (
            f"\n\n-- \n\n"
            "FomoSapiensCryptoDipHunter\nhttps://fomo.ropeaccess.pro\n\n"
            "StefanCryptoTradingBot\nhttps://stefan.ropeaccess.pro\n\n"
            "CodeCave\nhttps://cave.ropeaccess.pro\n"
        )
        send_email(email, ta_subject, ta_content)
        send_email(email, ai_subject, ai_content)

    messages.success(request, "Email sent successfully.")
    return redirect("show_technical_analysis")
