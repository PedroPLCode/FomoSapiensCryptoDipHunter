from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import atexit
import os
from fomo_sapiens.utils.logging import logger

SCHEDULER_LOCK_FILE = "fomo_sapiens/scheduler.lock"

class FomoSapiensConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fomo_sapiens'
    scheduler = None

    def ready(self):
        from hunter.utils import hunter_logic
        from fomo_sapiens.utils import logs_utils
        
        if os.path.exists(SCHEDULER_LOCK_FILE):
            logger.info("Scheduler is already running. Skipping initialization.")
            return

        if not FomoSapiensConfig.scheduler:
            scheduler = BackgroundScheduler(
                executors={'default': {'type': 'threadpool', 'max_workers': 1}}
            )
            FomoSapiensConfig.scheduler = scheduler
            scheduler.remove_all_jobs()

            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                'interval',
                minutes=1,
                id='every_hour_hunter_task',
                max_instances=1,
                misfire_grace_time=900,
                args=['1h']
            )
            
            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                'interval',
                hours=4,
                id='every_four_hour_hunter_task',
                max_instances=1,
                misfire_grace_time=900,
                args=['4h']
            )
            
            scheduler.add_job(
                hunter_logic.run_selected_interval_hunters,
                'interval',
                hours=24,
                id='every_day_hunter_task',
                max_instances=1,
                misfire_grace_time=900,
                args=['1d']
            )

            scheduler.add_job(
                logs_utils.send_daily_logs,
                'interval',
                hours=24,
                id='every_day_logs_task',
                max_instances=1,
                misfire_grace_time=900
            )

            scheduler.add_job(
                logs_utils.clear_logs,
                'interval',
                hours=24,
                id='every_day_cleaning_task',
                max_instances=1,
                misfire_grace_time=900
            )

            logger.info("Starting scheduler...")
            scheduler.start()

            open(SCHEDULER_LOCK_FILE, 'w').close()

            atexit.register(lambda: scheduler.shutdown())
            atexit.register(lambda: os.remove(SCHEDULER_LOCK_FILE))
