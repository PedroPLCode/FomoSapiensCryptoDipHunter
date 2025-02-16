from django.core.mail import send_mail
from .logging import logger
from .exception_handlers import exception_handler

@exception_handler(default_return=False)
def send_email(email, subject, body):
    """
    Sends an email to a specified recipient.

    This function uses Django's send_mail to send an email with the given subject and body
    to the specified email address. If an exception occurs, it logs the error
    and notifies the admin via email.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        Logs any exceptions encountered and notifies the admin.
    """
    try:
        send_mail(subject, body, 'your-email@example.com', [email])
        logger.info(f'Email "{subject}" to {email} sent successfully.')
        return True
    except Exception as e:
        logger.error(f"Error sending email to {email}. Error: {str(e)}")
        return False


def send_admin_email(subject, body):
    """
    Sends an email notification to all users with admin panel access.

    This function retrieves all users who have `is_superuser=True`
    and sends them an email with the given subject and body. If an exception
    occurs, it logs the error.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        Logs any exceptions encountered.
    """
    from django.apps import apps

    if apps.ready:
        from django.contrib.auth.models import User
    try:
        users = User.objects.filter(is_superuser=True)
        for user in users:
            success = send_email(user.email, subject, body)
            if not success:
                logger.error(f"Failed to send admin email to {user.email}. {subject} {body}")
    except Exception as e:
        logger.error(f"Exception in send_admin_email: {str(e)}")