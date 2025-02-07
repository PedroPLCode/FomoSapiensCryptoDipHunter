from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TechnicalAnalysisHunterForm
from .models import TechnicalAnalysisHunter

@login_required
def hunter_list(request):
    hunters = TechnicalAnalysisHunter.objects.filter(user=request.user)
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