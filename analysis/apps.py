from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AnalysisConfig(AppConfig):
    """
    Configuration for the 'analysis' application.

    This class is used to define the configuration of the 'analysis' app in the Django project.
    It specifies the default auto field for model primary keys and imports necessary signals 
    when the application is ready.

    Attributes:
        default_auto_field (str): The default field to use for auto-incrementing primary keys.
        name (str): The name of the Django app, which is 'analysis'.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'

    def ready(self):
        """
        Import signals when the app is ready.

        This method is automatically called by Django when the app is fully loaded.
        It ensures that the signals from the 'fomo_sapiens.utils.signals' module are imported
        and ready to be used.
        """
        import fomo_sapiens.utils.signals
        
        from django.contrib.sites.models import Site
        post_migrate.connect(self.set_site, sender=self)

    def set_site(self, sender, **kwargs):
        """
        Sets the site domain and name after migrations.

        This function ensures that the default site configuration is correctly set up
        after database migrations. It retrieves or creates a Site instance with ID 1
        and updates its domain and name.

        Args:
            sender (AppConfig): The application that triggered the signal.
            **kwargs: Additional keyword arguments passed by the signal.
        """
        from django.contrib.sites.models import Site
        site, created = Site.objects.get_or_create(id=1)
        site.domain = "fomosapienscryptodiphunter.com"
        site.name = "FomoSapiensCryptoDipHunter"
        site.save()