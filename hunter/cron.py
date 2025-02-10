from django_cron import CronJobBase, Schedule
from fomo_sapiens.utils.logs_utils import (
    send_daily_logs,
    clear_logs
)
from utils.hunter_logic import (
    run_selected_interval_hunters
)

class HourlyCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)  # co 60 minut
    code = 'hunter.hourly_cron_job'

    def do(self):
        run_selected_interval_hunters('1h')

class FourHoursCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=240)  # co 240 minut (4 godziny)
    code = 'hunter.four_hourly_cron_job'

    def do(self):
        run_selected_interval_hunters('4h')

class DailyCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=1440)  # codziennie
    code = 'hunter.daily_cron_job'

    def do(self):
        run_selected_interval_hunters('1d')
        send_daily_logs()
        clear_logs()