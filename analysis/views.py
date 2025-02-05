from django.shortcuts import render, redirect
from .forms import UserTechnicalAnalysisSettingsForm
from .models import User, UserTechnicalAnalysisSettings
from. utils.logging import logger
from .utils.api_utils import fetch_data
from .utils.calc_utils import calculate_ta_indicators
from .utils.plot_utils import plot_selected_ta_indicators

def update_technical_analysis_settings(request):

    user_settings, created = UserTechnicalAnalysisSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserTechnicalAnalysisSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('settings_updated')
    else:
        form = UserTechnicalAnalysisSettingsForm(instance=user_settings)

    return render(request, 'analysis/change.html', {'form': form})


def settings_updated(request):
    return render(request, 'analysis/updated.html')


def show_technical_analysis(request):
    """Widok analizy technicznej dostępny zarówno dla gości, jak i dla zalogowanych użytkowników."""

    if request.user.is_authenticated:
        user_settings, created = UserTechnicalAnalysisSettings.objects.get_or_create(
            user=request.user,
        )
    else:
        guest_user = User.objects.get(username='guest')
        user_settings, created = UserTechnicalAnalysisSettings.objects.get_or_create(
            user=guest_user,
        )

    df_fetched = fetch_data(symbol=user_settings.symbol, interval=user_settings.interval, lookback=user_settings.lookback)
    if df_fetched is None or df_fetched.empty:
        return render(request, 'analysis/show.html', {'error': 'Nie udało się pobrać danych'})

    df_calculated = calculate_ta_indicators(df_fetched, user_settings)
    if df_calculated is None or df_calculated.empty:
        return render(request, 'analysis/show.html', {'error': 'Nie udało się obliczyć analizy technicznej'})
    
    latest_data = df_calculated.iloc[-1].to_dict
    plot_url = plot_selected_ta_indicators(df_calculated, user_settings)

    return render(request, 'analysis/show.html', {'user_settings': user_settings, 'latest_data': latest_data, 'plot_url': plot_url})
