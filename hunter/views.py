from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from io import StringIO
import pandas as pd
from .forms import TechnicalAnalysisHunterForm
from .models import TechnicalAnalysisHunter
from fomo_sapiens.utils.exception_handlers import exception_handler
from fomo_sapiens.utils.logging import logger

@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def show_hunters_list(request):
    """
    View function to display a list of hunters associated with the logged-in user.
    Each hunter's data is processed to calculate technical analysis indicators and
    a plot URL is generated for each hunter.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered 'hunters_list.html' template with the hunters' data and plot URLs.
    """
    from analysis.utils.calc_utils import calculate_ta_indicators
    from analysis.utils.plot_utils import plot_selected_ta_indicators
    
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    for hunter in hunters:
        df_loaded = pd.read_json(StringIO(hunter.df))
        df_calculated = calculate_ta_indicators(df_loaded, hunter)
        plot_url = plot_selected_ta_indicators(df_calculated, hunter)
        hunter.plot_url = plot_url
    
    return render(request, 'hunter/hunters_list.html', {'hunters': hunters})


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def hunter_create_or_edit(request, pk=None):
    """
    View function to create a new hunter or edit an existing one. The hunter's
    data is stored in the form, validated, and saved to the database.

    Args:
        request: The HTTP request object.
        pk: The primary key of the hunter to edit (if provided).

    Returns:
        A rendered 'hunter_edit.html' template with the form for creating or editing a hunter.
    """
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
            return redirect('hunter:show_hunters_list')
    else:
        form = TechnicalAnalysisHunterForm(instance=hunter)

    return render(request, 'hunter/hunter_edit.html', {'form': form, 'hunter': hunter, 'title': title})


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def hunter_delete(request, pk):
    """
    View function to delete a hunter. The hunter is identified by the primary key.
    A confirmation page is shown before deletion.

    Args:
        request: The HTTP request object.
        pk: The primary key of the hunter to delete.

    Returns:
        A rendered 'hunter_delete.html' template with the hunter's data for confirmation.
    """
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if request.method == 'POST':
        hunter.delete()
        messages.success(request, 'Hunter deleted')
        return redirect('hunter:show_hunters_list')
    return render(request, 'hunter/hunter_delete.html', {'hunter': hunter})


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def remove_all_hunters(request):
    """
    View function to remove all hunters associated with the logged-in user.
    A confirmation page is shown before deletion of all hunters.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered 'hunters_remove.html' template showing all hunters to be removed.
    """
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    if request.method == 'POST':
        if hunters:
            for hunter in hunters:
                hunter.delete()
                logger.info(f'hunter {hunter.id} removed')
            messages.success(request, 'All hunters removed')
        else:
            messages.success(request, 'No hunters to remove')
        return redirect('hunter:show_hunters_list')
    return render(request, 'hunter/hunters_remove.html', {'hunters': hunters})


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def start_all_hunters(request):
    """
    View function to start all hunters associated with the logged-in user.
    The running state of each hunter is updated to True.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the 'show_hunters_list' view with a success message.
    """
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    if hunters:
        for hunter in hunters:
            hunter.running = True
            hunter.save()
            logger.info(f'hunter {hunter.id} started')
        messages.success(request, 'All hunters started')
    else:
        messages.success(request, 'No hunters to start')
        
    return redirect('hunter:show_hunters_list')


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def start_hunter(request, pk):
    """
    View function to start a specific hunter identified by its primary key.
    The running state of the hunter is updated to True.

    Args:
        request: The HTTP request object.
        pk: The primary key of the hunter to start.

    Returns:
        A redirect to the 'show_hunters_list' view with a success message.
    """
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if hunter:
        hunter.running = True
        hunter.save()
        logger.info(f'hunter {hunter.id} started')
        messages.success(request, f'Hunter {hunter.id} started')
    else:
        messages.success(request, 'No hunter found to start')
        
    return redirect('hunter:show_hunters_list')


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def stop_hunter(request, pk):
    """
    View function to stop a specific hunter identified by its primary key.
    The running state of the hunter is updated to False.

    Args:
        request: The HTTP request object.
        pk: The primary key of the hunter to stop.

    Returns:
        A redirect to the 'show_hunters_list' view with a success message.
    """
    hunter = get_object_or_404(TechnicalAnalysisHunter, pk=pk, user=request.user)
    if hunter:
        hunter.running = False
        hunter.save()
        logger.info(f'hunter {hunter.id} stopped')
        messages.success(request, f'Hunter {hunter.id} stopped')
    else:
        messages.success(request, 'No hunter found to stop')
        
    return redirect('hunter:show_hunters_list')


@exception_handler(default_return=lambda: redirect('show_hunters_list'))
@login_required
def stop_all_hunters(request):
    """
    View function to stop all hunters associated with the logged-in user.
    The running state of each hunter is updated to False.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the 'show_hunters_list' view with a success message.
    """
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
    
    if hunters:
        for hunter in hunters:
            hunter.running = False
            hunter.save()
            logger.info(f'hunter {hunter.id} stopped')
        messages.success(request, 'All hunters stopped')
    else:
        messages.success(request, 'No hunters to stop')
        
    return redirect('hunter:show_hunters_list')