import sys
import functools
import logging
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


def exception_handler(default_return=None):
    """
    Decorator to handle exceptions and provide a consistent logging and error reporting
    mechanism for wrapped functions.

    This decorator catches a set of predefined exceptions (e.g., IndexError, BinanceAPIException,
    ConnectionError, etc.) and logs them along with the function name where the exception occurred.
    In case of an exception, it also sends an email to the admin with the error details.

    If the exception is of an unhandled type, a generic exception handler is invoked to log and report
    the error.

    The decorator allows for two behaviors for the return value after an exception:
    1. A default return value (specified by the `default_return` parameter).
    2. A callable that is invoked if the exception occurs.

    If `default_return` is set to `exit`, the program will terminate with `sys.exit(1)`.

    Args:
        default_return (optional): The value to return in case of an exception.
                                    It can be:
                                    - A default value to return
                                    - A callable that will be executed if an exception occurs
                                    - `exit` to terminate the program on error

    Returns:
        The value from `default_return` or the result of the callable if defined.
        If `exit` is passed, the program will terminate.

    Example:
        @exception_handler(default_return="Fallback value")
        def risky_function():
            # Function that may raise an exception
            pass
    """

    def exception_handler_decorator(func):
        @functools.wraps(func)
        def exception_handler_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (
                IndexError,
                BinanceAPIException,
                ConnectionError,
                TimeoutError,
                ValueError,
                TypeError,
                FileNotFoundError,
            ) as e:
                exception_type = type(e).__name__
                logger.error(f"{exception_type} in {func.__name__}: {str(e)}")
                from .email_utils import send_admin_email

                send_admin_email(f"{exception_type} in {func.__name__}", str(e))
            except Exception as e:
                exception_type = "Exception"
                logger.error(f"{exception_type} in {func.__name__}: {str(e)}")
                from .email_utils import send_admin_email

                send_admin_email(
                    f"{exception_type} in {func.__name__}",
                    f"FomoSapiensCryptoDipHunter\n{exception_type} in {func.__name__}\n\n{str(e)}",
                )

            if default_return is exit:
                logger.error("sys.exit(1) Exiting program due to an error.")
                sys.exit(1)
            elif callable(default_return):
                return default_return()
            return default_return

        return exception_handler_wrapper

    return exception_handler_decorator
