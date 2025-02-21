from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
from fomo_sapiens.utils.logging import logger

SCHEDULER_LOCK_FILE = "fomo_sapiens/scheduler.lock"


class FomoSapiensConfig(AppConfig):
    """
    Configuration for the FomoSapiens Django app, handling the initialization
    and management of background tasks with APScheduler.

    This class is responsible for setting up the scheduler that runs periodic tasks,
    including the execution of trading hunters, logging tasks, and log cleaning.
    It ensures that the scheduler only runs once by creating a lock file.
    The tasks are scheduled to run at various intervals, with their respective
    logic implemented in the hunter and logs utilities.

    Attributes:
        default_auto_field (str): The default field type for auto-incrementing IDs in models.
        name (str): The name of the Django application.
        scheduler (BackgroundScheduler): The background scheduler instance that manages jobs.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "fomo_sapiens"
    scheduler = None

    def ready(self):
        """
        Initializes and starts the background scheduler for periodic tasks.

        This method runs when the application is ready and checks whether the
        scheduler is already running (by checking the existence of the lock file).
        If not, it initializes the `BackgroundScheduler`, adds jobs for the various
        tasks (e.g., executing hunters, sending logs), and starts the scheduler.

        Additionally, it ensures that the scheduler shuts down gracefully upon
        application exit and cleans up the lock file.

        Scheduled tasks include:
            - Running selected interval hunters every minute, every 4 hours, and daily.
            - Sending daily logs and clearing logs every 24 hours.
        """
        from hunter.utils import hunter_logic
        from fomo_sapiens.utils import logs_utils, db_utils

        if os.path.exists(SCHEDULER_LOCK_FILE):
            logger.info("Scheduler is already running. Skipping initialization.")
            return

        if not FomoSapiensConfig.scheduler:
            scheduler = BackgroundScheduler(
                executors={"default": {"type": "threadpool", "max_workers": 1}}
            )
            FomoSapiensConfig.scheduler = scheduler
            scheduler.remove_all_jobs()

            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                "interval",
                minutes=1,
                id="every_hour_hunter_task",
                max_instances=1,
                misfire_grace_time=900,
                args=["1h"],
            )

            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                "interval",
                hours=4,
                id="every_four_hour_hunter_task",
                max_instances=1,
                misfire_grace_time=900,
                args=["4h"],
            )

            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                "interval",
                hours=24,
                id="every_day_hunter_task",
                max_instances=1,
                misfire_grace_time=900,
                args=["1d"],
            )

            scheduler.add_job(
                logs_utils.send_daily_logs,
                "interval",
                hours=24,
                id="every_day_logs_task",
                max_instances=1,
                misfire_grace_time=900,
            )

            scheduler.add_job(
                logs_utils.clear_logs,
                "interval",
                hours=24,
                id="every_day_cleaning_task",
                max_instances=1,
                misfire_grace_time=900,
            )
            
            scheduler.add_job(
                db_utils.backup_database,
                'interval',
                hours=24,
                id='every_day_db_backup_task',
                max_instances=1,
                misfire_grace_time=900
            )

            logger.info("Starting scheduler...")
            scheduler.start()

            open(SCHEDULER_LOCK_FILE, "w").close()

            atexit.register(lambda: scheduler.shutdown())
            atexit.register(lambda: os.remove(SCHEDULER_LOCK_FILE))
