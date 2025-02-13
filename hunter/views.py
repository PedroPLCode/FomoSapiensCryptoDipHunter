from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from io import StringIO
import pandas as pd
from .forms import TechnicalAnalysisHunterForm
from .models import TechnicalAnalysisHunter
from fomo_sapiens.utils.logging import logger

@login_required
def hunter_list(request):
    from analysis.utils.calc_utils import calculate_ta_indicators
    from analysis.utils.plot_utils import plot_selected_ta_indicators
    
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    for hunter in hunters:
        df_loaded = pd.read_json(StringIO(hunter.df))
        df_calculated = calculate_ta_indicators(df_loaded, hunter)
    
        plot_url = plot_selected_ta_indicators(df_calculated, hunter)
        hunter.plot_url = plot_url
    
    return render(request, 'hunter/hunter_list.html', {'hunters': hunters})


@login_required
def hunter_create_or_edit(request, pk=None):
    if pk:
        title = 'Selected Hunter Settings:'
        hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    else:
        title = 'Create New Hunter:'
        hunter = None

    if request.method == "POST":
        form = TechnicalAnalysisHunterForm(request.POST, instance=hunter)
        if form.is_valid():
            hunter = form.save(commit=False)
            hunter.user = request.user
            hunter.save()
            messages.success(request, f'Hunter {"changed" if pk else "created"}')
            return redirect('hunter:hunter_list')
    else:
        form = TechnicalAnalysisHunterForm(instance=hunter)

    return render(request, 'hunter/hunter_edit.html', {'form': form, 'hunter': hunter, 'title': title})


@login_required
def hunter_delete(request, pk):
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if request.method == 'POST':
        hunter.delete()
        messages.success(request, 'Hunter deleted')
        return redirect('hunter:hunter_list')
    return render(request, 'hunter/hunter_delete.html', {'hunter': hunter})


@login_required
def start_all_hunters(request):
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    if hunters:
        for hunter in hunters:
            hunter.running = True
            hunter.save()
            logger.info(f'hunter {hunter.id} stoped')
        messages.success(request, 'All hunters started')
    else:
        messages.success(request, 'No hunters to start')
        
    return redirect('hunter:hunter_list')


@login_required
def start_hunter(request, pk):
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if hunter:
        hunter.running = True
        hunter.save()
        logger.info(f'hunter {hunter.id} started')
        messages.success(request, f'Hunter {hunter.id} started')
    else:
        messages.success(request, 'No hunter found to start')
        
    return redirect('hunter:hunter_list')


@login_required
def stop_hunter(request, pk):
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if hunter:
        hunter.running = False
        hunter.save()
        logger.info(f'hunter {hunter.id} stoped')
        messages.success(request, f'Hunter {hunter.id} stopped')
    else:
        messages.success(request, 'No hunter found to stop')
        
    return redirect('hunter:hunter_list')


@login_required
def stop_all_hunters(request):
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    if hunters:
        for hunter in hunters:
            hunter.running = False
            hunter.save()
            logger.info(f'hunter {hunter.id} stoped')
        messages.success(request, 'All hunters stopped')
    else:
        messages.success(request, 'No hunters to stop')
        
    return redirect('hunter:hunter_list')