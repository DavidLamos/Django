from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        # Attempt to import signals and log any errors
        try:
            import dashboard.signals
        except ImportError as e:
            # Log the error with the logger
            logger.error(f"Error importing dashboard.signals: {e}")
