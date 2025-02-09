from django.shortcuts import render, redirect
from django.contrib import messages

def custom_404_view(request, exception):
    messages.success(request, '404 > home_page')
    return redirect("/")

def home_page(request):
    from analysis.utils.fetch_utils import fetch_server_time, fetch_system_status
    server_time = fetch_server_time()
    system_status = fetch_system_status()
    return render(request, 'home/home_page.html', {'server_time': server_time, 'system_status': system_status})