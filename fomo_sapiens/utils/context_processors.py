import platform
import subprocess
import sys
import numpy as np
import pandas as pd
from django.db import connection
from django.utils import timezone
from typing import Dict


def inject_date_and_time(request) -> Dict[str, str]:
    """
    Injects current date and time into the context for use in templates.
    """
    try:
        date_and_time = timezone.now()
        date_and_time = date_and_time.replace(tzinfo=None)
    except Exception as e:
        date_and_time = f"Error retrieving current time: {e}"
    return {"date_and_time": str(date_and_time.strftime('%Y-%m-%d %H:%M:%S'))}


def inject_user_agent(request) -> Dict[str, str]:
    """
    Injects the User-Agent header of the request into the context for use in templates.
    """
    try:
        user_agent = request.META.get("HTTP_USER_AGENT", "User-Agent not available")
    except Exception as e:
        user_agent = f"Error retrieving user agent: {e}"
    return {"user_agent": user_agent}


def inject_system_info(request) -> Dict[str, str]:
    """
    Injects the system's name, version, and release information into the context for use in templates.
    """
    try:
        system_name = platform.system()
        system_version = platform.version()
        release = platform.release()
    except Exception as e:
        system_name = f"Error retrieving system info: {e}"
    return {"system_info": f"{system_name} {release} {system_version}"}


def inject_system_uptime(request) -> Dict[str, str]:
    """
    Injects the system's uptime into the context for use in templates.
    """
    try:
        uptime = subprocess.check_output(["/usr/bin/uptime"], text=True).strip()
    except Exception as e:
        uptime = f"Error retrieving system uptime: {e}"
    return {"system_uptime": uptime}


def inject_python_version(request) -> Dict[str, str]:
    """
    Injects the Python version into the context for use in templates.
    """
    try:
        python_version = sys.version
    except Exception as e:
        python_version = f"Error retrieving python version: {e}"
    return {"python_version": python_version}


def inject_django_version(request) -> Dict[str, str]:
    """
    Injects the django version into the context for use in templates.
    """
    try:
        django_info = __import__("django").__version__
    except Exception as e:
        django_info = f"Error retrieving django version: {e}"
    return {"django_version": django_info}


def inject_numpy_version(request) -> Dict[str, str]:
    """
    Injects the version of NumPy into the context for use in templates.
    """
    try:
        numpy_version = np.__version__
    except Exception as e:
        numpy_version = f"Error retrieving numpy version: {e}"
    return {"numpy_version": numpy_version}


def inject_pandas_version(request) -> Dict[str, str]:
    """
    Injects the version of Pandas into the context for use in templates.
    """
    try:
        pandas_version = pd.__version__
    except Exception as e:
        pandas_version = f"Error retrieving pandas version: {e}"
    return {"pandas_version": pandas_version}


def inject_db_info(request) -> Dict[str, str]:
    """
    Injects the database engine type into the context for use in templates.
    """
    try:
        db_dialect = connection.vendor
    except Exception as e:
        db_dialect = f"Error retrieving db info: {e}"
    return {"db_engine": db_dialect}
