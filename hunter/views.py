from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from io import StringIO
import pandas as pd
from .forms import TechnicalAnalysisHunterForm
from .models import TechnicalAnalysisHunter

@login_required
def hunter_list(request):
    from analysis.utils.calc_utils import calculate_ta_indicators
    from analysis.utils.plot_utils import plot_selected_ta_indicators, prepare_selected_indicators_list
    from analysis.utils.plot_utils import get_bot_specific_plot_indicators
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    for hunter in hunters:
        df_loaded = pd.read_json(StringIO(hunter.df))
        df_calculated = calculate_ta_indicators(df_loaded, hunter)
    
        plot_url = plot_selected_ta_indicators(df_calculated, hunter)
        hunter.plot_url = plot_url
    
    return render(request, 'hunter/hunter_list.html', {'hunters': hunters})


@login_required
def hunter_create(request):
    title = 'Create New Hunter:'
    if request.method == "POST":
        form = TechnicalAnalysisHunterForm(request.POST)
        if form.is_valid():
            hunter = form.save(commit=False)
            hunter.user = request.user
            hunter.save()
            return redirect('hunter:hunter_list')
    else:
        form = TechnicalAnalysisHunterForm()

    return render(request, 'hunter/hunter_edit.html', {'form': form, 'title': title})


@login_required
def hunter_edit(request, pk):
    title = 'Selected Hunter Settings:'
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TechnicalAnalysisHunterForm(request.POST, instance=hunter)
        if form.is_valid():
            form.save()
            return redirect('hunter:hunter_list')
    else:
        form = TechnicalAnalysisHunterForm(instance=hunter)
    return render(request, 'hunter/hunter_edit.html', {'form': form, 'hunter': hunter, 'title': title})


@login_required
def hunter_delete(request, pk):
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if request.method == 'POST':
        hunter.delete()
        return redirect('hunter:hunter_list')
    return render(request, 'hunter/hunter_delete.html', {'hunter': hunter})