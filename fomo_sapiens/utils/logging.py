"""
Logging configuration for the application.

This module sets up a logging system for the application, enabling the capture of debug-level logs
to a file (`django.log`) for general application activities. Additional log files can be added for
specific services (e.g., `gunicorn.log` for Gunicorn-related logs).

The main logger is configured to capture logs at the DEBUG level, ensuring that all logs from
DEBUG level and above (INFO, WARNING, ERROR, CRITICAL) are recorded.

- A `FileHandler` is used to write logs to the specified log file (`django.log`).
- A custom log format is applied that includes the timestamp, log level, and the actual log message.

Logs are written to the `app_log_filename` file by default. The `gunicorn_log_filename` is provided as a placeholder for additional logging setups.

Log rotation and handling for multiple loggers (e.g., for Gunicorn) may be configured separately.

Log format:
    %(asctime)s %(levelname)s: %(message)s

Log levels:
    DEBUG, INFO, WARNING, ERROR, CRITICAL

Example usage:
    logger.debug("This is a debug message.")
    logger.info("This is an informational message.")
    logger.error("This is an error message.")
"""

import logging

app_log_filename = "django.log"
gunicorn_log_filename = "gunicorn.log"
logs = [app_log_filename, gunicorn_log_filename]

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)

general_handler = logging.FileHandler(app_log_filename)
general_handler.setLevel(logging.DEBUG)
general_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
general_handler.setFormatter(general_formatter)

logger.addHandler(general_handler)
