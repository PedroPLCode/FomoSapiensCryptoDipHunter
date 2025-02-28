from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from analysis.utils.fetch_utils import fetch_server_time, fetch_system_status


def custom_404_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Handles the custom 404 error page by displaying a success message
    and redirecting the user to the home page.

    This view is triggered when a 404 error occurs. It sends a success
    message indicating the error and redirects the user to the home page.

    Args:
        request (HttpRequest): The request object.
        exception (Exception): The exception that caused the 404 error.

    Returns:
        HttpResponse: A redirect to the home page.
    """
    server_time = fetch_server_time()
    system_status = fetch_system_status()
    return render(
        request, 
        "error_404.html", 
        {"server_time": server_time, "system_status": system_status},
        status=404,
    )

def home_page(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page with server time and system status.

    This view fetches the current server time and system status,
    then renders the home page template with this information.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered home page with server time and system status.
    """
    server_time = fetch_server_time()
    system_status = fetch_system_status()
    return render(
        request,
        "home/home_page.html",
        {"server_time": server_time, "system_status": system_status},
    )
