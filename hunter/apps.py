from django.apps import AppConfig


class HunterConfig(AppConfig):
    """
    Configuration for the 'hunter' Django app.

    This class is used to configure the 'hunter' app during the startup of the Django project.
    It includes settings for the app's default auto field type and its name.

    Attributes:
        default_auto_field (str): The default field type for auto-generated fields, set to BigAutoField.
        name (str): The name of the app, which is 'hunter'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "hunter"
