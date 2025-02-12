from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from io import StringIO
import pandas as pd
from .forms import TechnicalAnalysisSettingsForm
from .models import User, TechnicalAnalysisSettings
from fomo_sapiens.utils.logging import logger
from .utils.fetch_utils import fetch_and_save_df
from .utils.calc_utils import calculate_ta_indicators
from .utils.plot_utils import plot_selected_ta_indicators, prepare_selected_indicators_list

@login_required
def update_technical_analysis_settings(request):

    user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TechnicalAnalysisSettingsForm(request.POST, instance=user_ta_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twoje ustawienia zostały zapisane!')
            return redirect('show_technical_analysis')
    else:
        form = TechnicalAnalysisSettingsForm(instance=user_ta_settings)

    return render(request, 'analysis/change_settings.html', {'form': form})


@login_required
def refresh_data(request):
    user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)
    fetch_and_save_df(user_ta_settings)
    messages.success(request, 'Data refreshed')
    return redirect('show_technical_analysis')


def show_technical_analysis(request):
    """Widok analizy technicznej dostępny zarówno dla gości, jak i dla zalogowanych użytkowników."""

    if request.user.is_authenticated:
            user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=request.user)
    else:
        guest_user, created = User.objects.get_or_create(username='guest')
        user_ta_settings, created = TechnicalAnalysisSettings.objects.get_or_create(user=guest_user)

    indicators_list = ['close', 'rsi', 'cci', 'mfi', 'macd', 'ema', 'boll', 'stoch', 'stoch-rsi', 
                       'ma50', 'ma200', 'adx', 'atr', 'psar', 'vwap', 'di']

    if request.method == 'POST':
        selected_indicators = request.POST.getlist('indicators')
        user_ta_settings.selected_plot_indicators = ','.join(selected_indicators)
        user_ta_settings.save()

    df_loaded = pd.read_json(StringIO(user_ta_settings.df))
    if df_loaded is None or df_loaded.empty:
        return render(request, 'analysis/show.html', {'error': 'Nie udało się pobrać danych'})

    df_calculated = calculate_ta_indicators(df_loaded, user_ta_settings)
    if df_calculated is None or df_calculated.empty:
        return render(request, 'analysis/show.html', {'error': 'Nie udało się obliczyć analizy technicznej'})

    latest_data = df_calculated.iloc[-1].to_dict()
    previous_data = df_calculated.iloc[-2].to_dict()
    
    selected_indicators_list = prepare_selected_indicators_list(user_ta_settings.selected_plot_indicators)
    plot_url = plot_selected_ta_indicators(df_calculated, user_ta_settings)
    
    return render(request, 'analysis/show_analysis.html', {
        'user_ta_settings': user_ta_settings,
        'latest_data': latest_data,
        'previous_data': previous_data,
        'plot_url': plot_url,
        'selected_indicators_list': selected_indicators_list,
        'indicators': indicators_list 
    })